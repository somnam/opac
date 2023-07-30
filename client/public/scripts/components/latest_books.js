"use strict";

import Field from '../widgets/field.js';
import DataTable from '../widgets/data_table.js';
import Storage from '../app/storage.js';
import { InternalServerError } from '../app/exception.js';


class LatestBooks extends Field {
    template = `
      <fieldset id="latest-books-fields">
        <div id="latest-books-container" class="nes-container with-title mb-4">
          <h3 class="title">Search results</h3>
          <div id="latest-books-table" class="nes-table-responsive"></div>
        </div>

        <button class="nes-btn is-primary btn-block mb-4" id="catalogs-btn">
          To Catalogs
        </button>

        <button class="nes-btn btn-block mb-4" id="go-back-btn">
          Back
        </button>
      </fieldset>
    `;

    headers = [
        'title',
        'author',
        'isbn',
    ]

    constructor(transport) {
        super(transport);

        this.dataTable = new DataTable('latest-books', this.headers);
    }

    static toString() { return 'latest-books' }

    onInit() {
        const message = {
            "catalog": Storage.getDecoded('catalog'),
            "included_shelves": Storage.getDecoded('include-latest-book-shelves'),
            "excluded_shelves": Storage.getDecoded('exclude-latest-book-shelves'),
        };

        this.transport.post('latest-books/search', message)
            .then(response => {
                if (!response.ok) {
                    throw new InternalServerError(response.status);
                } else {
                    return response.json();
                }
            })
            .then(result => {
                if (result !== null) {
                    Storage.setEncoded('latest-books', result);
                    super.onInit();
                } else {
                    console.log("No latest books found.")
                }
            })
            .catch(error => console.error(error));
    }

    onRender() {
        this.addEvents();
        this.update();
    }

    onBack() {
        this.emit(`${this}-hide`);
        this.emit('exclude-latest-book-shelves-init');
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
        const catalogsBtn = document.querySelector('#catalogs-btn');
        catalogsBtn.addEventListener('click', (event) => {
            this.catalogsBtnEventListener(event);
        });

        const backBtn = document.querySelector('#latest-books-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));
    }

    catalogsBtnEventListener(event) {
        event.preventDefault();
        this.emit(`${this}-hide`);
        this.emit('catalogs-init');
    }

    backBtnListener(event) {
        event.preventDefault();
        this.emit(`${this}-back`);
    }
}


export default LatestBooks;
