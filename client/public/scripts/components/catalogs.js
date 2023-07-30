"use strict";

import Field from '../widgets/field.js';
import Storage from '../app/storage.js';
import RadioList from '../widgets/radio_list.js';
import LoadingBtn from '../widgets/loading_btn.js';


class Catalogs extends Field {
    template = `
    <fieldset id="catalogs-fields">
        <div id="catalog-list-container" class="nes-container with-title mb-4">
          <h3 class="title">Catalog</h3>
          <div class="item" id="catalog-list">
          </div>
        </div>

        <button class="nes-btn is-primary btn-block mb-4" id="select-catalog-btn">
          Next
        </button>

        <button class="nes-btn btn-block mb-4" id="go-back-btn">
          Back
        </button>
    </fieldset>
    `;

    items = [
        {"name": "Opac (Bielsko-Biała)", "value": "4949"},
        {"name": "Wojewódzka Biblioteka Publiczna (Kraków)", "value": "5004"},
    ];

    static toString() { return 'catalogs' }

    onRender() {
        Storage.setEncoded('catalogs', {"items": this.items});

        this.radioList = new RadioList('catalogs', 'catalog');

        this.loadingBtn = new LoadingBtn('#select-catalog-btn');

        this.addEvents();
        this.radioList.update();
    }

    onNext() {
        const catalog = this.radioList.checked;

        Storage.setEncoded('catalog', catalog);

        this.emit('catalogs-hide');
        this.emit('activities-init');
    }

    onBack() {
        Storage.remove('catalogs', 'catalog');

        this.emit('catalogs-hide');
        this.emit('start-init');
    }

    addEvents() {
        const searchCatalogBtn = document.querySelector('#select-catalog-btn');
        searchCatalogBtn.addEventListener('click', (event) => {
            this.selectCatalogBtnListener(event);
        });

        const backBtn = document.querySelector('#catalogs-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));

    }

    selectCatalogBtnListener(event) {
        event.preventDefault();

        this.loadingBtn.show();

        this.emit('catalogs-next');
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('catalogs-back');
    }
}


export default Catalogs;
