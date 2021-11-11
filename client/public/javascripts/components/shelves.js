import Field from './widgets/field.js';
import Storage from '../app/storage.js';
import RadioList from './widgets/radio_list.js';
import LoadingBtn from './widgets/loading_btn.js';
import Pager from './widgets/pager.js';


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
        super();

        this.transport = transport;

        this.on('shelves-show', () => this.onShow());

        this.on('shelves-hide', () => this.remove());

        this.on('shelves-paginate', (page) => this.onPaginate(page));

        this.on(`shelves-request`, (message) => this.onRequest(message));

        this.on('shelves-data', () => this.onData());

        this.on('shelves-next', () => this.onNext());

        this.on('shelves-back', () => this.onBack());
    }

    static toString() { return 'shelves' }

    onRequest(message) {
        this.transport.recv('shelves', message)
        .then(() => this.emit('shelves-data'))
        .catch(error => console.error(error));
    }

    onData() {
        this.emit('confirm-profile-hide');
        this.emit('shelves-show');
    }

    onShow() {
        this.render()
            .then(() => {
                this.radioList = new RadioList('shelves', 'shelf');

                this.pager = new Pager('shelf-list-container', 'shelves-paginate');

                this.loadingBtn = new LoadingBtn('#select-shelf-btn');

                this.addEvents();
                this.update();
            })
            .catch(error => console.error(error));
    }

    onNext() {
        const shelf = this.radioList.checked;

        Storage.setEncoded('shelf', shelf);

        this.emit('search-catalog-request');
    }

    onBack() {
        Storage.remove('shelf', 'shelves');

        this.emit('shelves-hide');
        this.emit('confirm-profile-show');
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
        const profile = Storage.getDecoded('profile');
        this.emit(
            'shelves-request',
            {name: profile.name, value: profile.value, page: page},
        )
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
