import Field from './widgets/field.js';
import DataTable from './widgets/data_table.js';
import Storage from '../app/storage.js';


class LatestBooks extends Field {
    template = `
      <fieldset id="latest-books-fields">
        <div id="latest-books-container" class="nes-container with-title mb-4">
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

        this.dataTable = new DataTable('latest-books', this.headers);
    }

    static toString() { return 'latest-books' }

    onRequest() {
        const message = {
            "catalog": Storage.getDecoded('catalog'),
            "included_shelves": Storage.getDecoded('include-latest-book-shelves'),
            "excluded_shelves": Storage.getDecoded('exclude-latest-book-shelves'),
        };

        this.transport.post('latest-books/search', message)
            .then(response => response.json())
            .then(result => {
                Storage.setEncoded('latest-books', result);
                this.emit('latest-books-data');
            })
            .catch(error => console.error(error));
    }

    onData() {
        if (Storage.getDecoded('latest-books') !== null) {
            super.onData();
        } else {
            console.log("No latest books found.")
        }
    }

    onRender() {
        this.addEvents();
        this.update();
    }

    onBack() {
        this.emit('latest-books-hide');
        this.emit('exclude-latest-book-shelves-request');
    }

    update() {
        const searchResult = Storage.getDecoded('latest-books');

        if (searchResult) {
            this.dataTable.update(searchResult.items);
        } else {
            console.log("No results.");
        }
    }

    addEvents() {
        const backBtn = document.querySelector('#latest-books-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('latest-books-back');
    }
}


export default LatestBooks;
