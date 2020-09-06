import {FieldMixin} from '../mixin/field.js';
import {EventEmitter} from '../mixin/event_emitter.js';
import {RadioList, RadioListParams} from '../widgets/radio_list.js';


class Catalogs {
    constructor() {
        this.radio_list = new RadioList('catalog-list-container', 'catalog');

        this.on('catalogs-show', () => this.onCatalogsShow());

        this.on('catalogs-hide', () => this.hide('#catalogs-fields'));

        this.on('catalogs-results', () => this.emit('catalogs-show'));
    }

    onDomLoaded() {
        const backBtn = document.querySelector('#catalogs-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));

        const searchCatalogBtn = document.querySelector('#search-catalog-btn');
        searchCatalogBtn.addEventListener('click', (event) => {
            this.selectCatalogBtnListener(event);
        });
    }

    onCatalogsShow() {
        let catalogsJson = this.storage.getItem('catalogs');
        if (catalogsJson !== null) {
            this.radio_list.update(new RadioListParams(
                JSON.parse(catalogsJson),
                this.storage.getItem('catalog'),
            ));
        }

        this.show('#catalogs-fields');
    }

    backBtnListener(event) {
        event.preventDefault();

        this.storage.removeItem('catalog');
        this.storage.removeItem('catalogs');

        this.emit('catalogs-hide');
        this.emit('shelves-show');
    }

    selectCatalogBtnListener(event) {
        event.preventDefault();

        const value = document.querySelector('input[name="catalog"]:checked').value;

        const catalogs = JSON.parse(this.storage.getItem('catalogs'));

        const catalogIndex = catalogs.findIndex((elem) => elem.value === value);

        const catalog = catalogs[catalogIndex];

        this.storage.setItem('catalog', JSON.stringify(catalog));
    }
}


Object.assign(Catalogs.prototype, EventEmitter);
Object.assign(Catalogs.prototype, FieldMixin);

export default Catalogs;
