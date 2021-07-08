import Field from './widgets/field.js';
import Storage from '../app/storage.js';
import RadioList from './widgets/radio_list.js';


class Catalogs extends Field {
    template = `
        <template>
          <fieldset id="catalogs-fields">
            <div id="catalog-list-container" class="nes-container with-title mb-4">
              <h3 class="title">Catalog</h3>
              <div class="item" id="catalog-list">
              </div>
            </div>

            <button class="nes-btn is-primary btn-block mb-4" id="select-catalog-btn">
              Next
            </button>
          </fieldset>
        </template>
    `;

    items = [
        {"name": "Opac (Bielsko-Biała)", "value": "4949"},
        {"name": "Wojewódzka Biblioteka Publiczna (Kraków)", "value": "5004"},
    ];

    constructor(transport) {
        super();

        this.transport = transport;

        Storage.setEncoded('catalogs', {"items": this.items});

        this.radioList = new RadioList('catalogs', 'catalog');

        this.on('catalogs-show', () => this.onShow());

        this.on('catalogs-hide', () => this.remove());

        this.on('catalogs-next', () => {
            this.emit('catalogs-hide');
            this.emit('activities-show');
        });
    }

    static toString() { return 'catalogs' }

    onShow() {
        this.render()
            .then(() => {
                this.addEvents();
                this.radioList.update();
            })
            .catch(error => console.error(error));
    }

    addEvents() {
        const searchCatalogBtn = document.querySelector('#select-catalog-btn');
        searchCatalogBtn.addEventListener('click', (event) => {
            this.selectCatalogBtnListener(event);
        });
    }

    selectCatalogBtnListener(event) {
        event.preventDefault();

        const catalog = this.radioList.checked;

        Storage.setEncoded('catalog', catalog);

        this.showLoading('#select-catalog-btn');

        this.emit('catalogs-next');
    }
}


export default Catalogs;
