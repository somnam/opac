"use strict";

import Field from '../widgets/field.js';
import Storage from '../app/storage.js';
import RadioList from '../widgets/radio_list.js';
import LoadingBtn from '../widgets/loading_btn.js';
import Pager from '../widgets/pager.js';
import { NotFoundError, InternalServerError } from '../app/exception.js';


class Shelves extends Field {
    template = `
      <fieldset id="shelves-fields">
        <div id="shelf-list-container" class="nes-container with-title mb-4">
          <h3 class="title">Shelf</h3>
          <div class="item" id="shelf-list">
          </div>
        </div>

        <button class="nes-btn is-primary btn-block mb-4" id="select-shelf-btn">
          Search
        </button>

        <button class="nes-btn btn-block mb-4" id="go-back-btn">
          Back
        </button>
      </fieldset>
    `;

    constructor(transport) {
        super(transport);

        this.on('shelves-paginate', (page) => this.onPaginate(page));
    }

    static toString() { return 'shelves' }

    onInit(message) {
        const profile = Storage.getDecoded('profile');
        this.transport.post(`profile/${profile.uuid}/shelves/search`, message)
            .then(response => {
                if (response.status === 404) {
                    throw new NotFoundError();
                }
                if (!response.ok) {
                    throw new InternalServerError(response.status);
                } else {
                    return response.json();
                }
            })
            .then((result) => {
                if (result.items.length !== 0) {
                    Storage.setEncoded('shelves', result);
                } else {
                    Storage.remove('shelves');
                }
                super.onInit();
            })
            .catch(error => console.error(error));
    }

    onRender() {
        this.radioList = new RadioList('shelves', 'shelf');

        this.pager = new Pager('shelf-list-container', 'shelves-paginate');

        this.loadingBtn = new LoadingBtn('#select-shelf-btn');

        this.addEvents();
        this.update();
    }

    onNext() {
        const shelf = this.radioList.checked;

        Storage.setEncoded('shelf', shelf);

        this.emit('search-catalog-init');
    }

    onBack() {
        Storage.remove('shelf', 'shelves');

        this.emit('shelves-hide');
        this.emit('activities-init');
    }

    update() {
        this.radioList.update();

        const shelves = Storage.getDecoded('shelves');
        if (shelves !== null) {
            this.pager.update(shelves.prev_page, shelves.next_page);
        }
    }

    addEvents() {
        const backBtn = document.querySelector('#shelves-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));

        const selectShelfBtn = document.querySelector('#select-shelf-btn');
        selectShelfBtn.addEventListener('click', (event) => {
            this.selectShelfBtnListener(event);
        });
    }

    onPaginate(page) {
        this.emit('shelves-init', {page: page})
    }

    selectShelfBtnListener(event) {
        event.preventDefault();

        this.loadingBtn.show();

        this.emit('shelves-next');
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('shelves-back');
    }
}


export default Shelves;
