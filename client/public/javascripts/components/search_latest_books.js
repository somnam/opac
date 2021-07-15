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

        this.on(`search-latest-books-request`, (message) => {
            this.transport.send('search-latest-books', message);

            Storage.set('latestBooksProgress', true);

            this.emit('search-latest-books-show');
        });

        this.on('search-latest-books-show', () => this.onShow());

        this.on('search-latest-books-hide', () => this.remove());

        this.on('search-latest-books-results', () => {
            Storage.remove('latestBooksProgress');

            if (Storage.getDecoded('latestBooks') !== null) {
                this.emit('search-latest-books-show');
            } else {
                console.log("No latest books found.")
            }
        });

        this.on('search-latest-books-back', () => {
            this.emit('search-latest-books-hide');
            this.emit('confirm-profile-show');
        });
    }

    static toString() { return 'search-latest-books' }

    onStart() {
        const catalog = Storage.getDecoded('catalog');

        switch(catalog ? catalog.value : null) {
            case "4949":
                this.emit('activities-hide');
                this.emit('in-development-show', 'activities');
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

    onShow() {
        this.render()
            .then(() => {
                this.addEvents();
                this.update();
            })
            .catch(error => console.error(error));
    }

    update() {
        const inProgress = Storage.get('latestBooksProgress');
        const searchResult = Storage.getDecoded('latestBooks');

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

        Storage.remove('latestBooks', 'latestBooksProgress');

        this.emit('search-latest-books-back');
    }
}


Object.assign(SearchLatestBooks.prototype, EventEmitter);


export default SearchLatestBooks;
