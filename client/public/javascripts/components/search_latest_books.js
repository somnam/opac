import Field from './widgets/field.js';
import DataTable from './widgets/data_table.js';
import Loading from './widgets/loading.js';
import Storage from '../app/storage.js';
import {EventEmitter} from '../mixin/event_emitter.js';


class SearchLatestBooks extends Field {
    template = `
      <fieldset id="search-latest-books-fields">
        <div id="search-latest-books-container" class="nes-container with-title mb-4">
          <h3 class="title">Search results</h3>
          <div id="latest-books-table" class="nes-table-responsive"></div>
        </div>

        <button class="nes-btn btn-block mb-4" id="go-back-btn">
          Back
        </button>
      </fieldset>
    `;

    headers = [
        'title',
        'author',
        'category',
        'pages'
    ]

    details = [
        'subtitle',
        'original_title',
        'isbn',
        'release'
    ]

    constructor(transport) {
        super();

        this.transport = transport;

        this.loading = new Loading('#search-latest-books-container');

        this.dataTable = new DataTable('latest-books', this.headers);

        this.on('search-latest-books-start', () => this.onStart());

        this.on(`search-latest-books-request`, () => this.onRequest());

        this.on(`search-latest-books-data`, () => this.onData());

        this.on('search-latest-books-show', () => this.onShow());

        this.on('search-latest-books-hide', () => this.remove());

        this.on('search-latest-books-back', () => this.onBack());
    }

    static toString() { return 'search-latest-books' }

    onStart() {
        const catalog = Storage.getDecoded('catalog');

        switch(catalog ? catalog.value : null) {
            case "4949":
                this.emit('activities-hide');
                this.emit('in-development-show');
                break;
            case "5004":
                this.emit('activities-hide');
                this.emit('search-profile-show');
                break;
            default:
                console.error("No catalog defined.");
                break;
        }
    }

    onRequest() {
        const message = {
            "catalog": Storage.getDecoded('catalog'),
            "included_shelves": Storage.getDecoded('include-latest-book-shelves'),
            "excluded_shelves": Storage.getDecoded('exclude-latest-book-shelves'),
        };

        this.transport.fetch('search-latest-books', message)
            .then(() => this.emit('search-latest-books-data'))
            .catch(error => console.error(error));

        Storage.set('latest-books-progress', true);

        this.emit('search-latest-books-show');
    }

    onData() {
        Storage.remove('latest-books-progress');

        if (Storage.getDecoded('latest-books') !== null) {
            this.emit('search-latest-books-show');
        } else {
            console.log("No latest books found.")
        }
    }

    onShow() {
        this.render()
            .then(() => {
                this.addEvents();
                this.update();
            })
            .catch(error => console.error(error));
    }

    onBack() {
        Storage.remove('latest-books', 'latest-books-progress');

        this.emit('search-latest-books-hide');
        this.emit('exclude-latest-book-shelves-show');
    }

    update() {
        const inProgress = Storage.get('latest-books-progress');
        const searchResult = Storage.getDecoded('latest-books');

        if (inProgress) {
            this.loading.show();
            this.dataTable.update();
        } else if (searchResult) {
            this.loading.hide();
            this.dataTable.update(searchResult.items);
        } else {
            console.log("No results.");
        }
    }

    addEvents() {
        const backBtn = document.querySelector('#search-latest-books-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('search-latest-books-back');
    }
}


Object.assign(SearchLatestBooks.prototype, EventEmitter);


export default SearchLatestBooks;
