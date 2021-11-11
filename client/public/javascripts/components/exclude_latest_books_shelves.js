import Field from './widgets/field.js';
import Storage from '../app/storage.js';
import CheckboxList from './widgets/checkbox_list.js';
import Pager from './widgets/pager.js';


export default class ExcludeLatestBooksShelves extends Field {
    template = `
    <fieldset id="exclude-latest-book-shelves-fields">
        <div id="shelf-list-container" class="nes-container with-title mb-4">
            <h3 class="title">Exclude shelves</h3>
            <div class="item" id="exclude-latest-book-shelves-list"></div>
        </div>

        <button class="nes-btn is-primary btn-block mb-4" id="exclude-shelfs-btn">
            Next
        </button>

        <button class="nes-btn btn-block mb-4" id="go-back-btn">
            Back
        </button>
    </fieldset>
    `;

    constructor(transport) {
        super();

        this.transport = transport;

        this.on('exclude-latest-book-shelves-show', () => this.onShow());

        this.on('exclude-latest-book-shelves-hide', () => this.remove());

        this.on('exclude-latest-book-shelves-paginate', (page) => this.onPaginate(page));

        this.on(`exclude-latest-book-shelves-request`, (message) => this.onRequest(message));

        this.on(`exclude-latest-book-shelves-data`, () => this.onData());

        this.on('exclude-latest-book-shelves-next', () => this.onNext());

        this.on('exclude-latest-book-shelves-back', () => this.onBack());
    }

    static toString() { return 'exclude-latest-book-shelves' }

    onRequest(message) {
        const shelves = Storage.getDecoded('shelves');

        const showCurrentPage = (message.page === undefined || shelves.page === message.page);

        if (shelves && showCurrentPage) {
            this.emit('exclude-latest-book-shelves-data');
        } else {
            this.transport.recv('shelves', message)
                .then(() => this.emit('exclude-latest-book-shelves-data'))
                .catch(error => console.error(error));
        }
    }

    onData() {
        this.emit('include-latest-book-shelves-hide');
        this.emit('exclude-latest-book-shelves-show');
    }

    onShow() {
        this.render()
            .then(() => {
                this.checkboxList = new CheckboxList(
                    'shelves',
                    'exclude-latest-book-shelves',
                    this.filterIncluded,
                );

                this.pager = new Pager(
                    'shelf-list-container',
                    'exclude-latest-book-shelves-paginate',
                );

                this.addEvents();
                this.update();
            })
            .catch(error => console.error(error));
    }

    onNext() {
        const shelves = this.checkboxList.checked;

        Storage.setEncoded('exclude-latest-book-shelves', shelves);

        this.emit('exclude-latest-book-shelves-hide');
        this.emit('search-latest-books-request');
    }

    onBack() {
        Storage.remove('exclude-latest-book-shelves');

        this.emit('exclude-latest-book-shelves-hide');
        this.emit('include-latest-book-shelves-show');
    }

    filterIncluded() {
        const includedValues = Storage.getDecoded('include-latest-book-shelves').map(
            shelf => shelf.value
        );
        const shelves = Storage.getDecoded('shelves');

        return shelves.items.filter(shelf => includedValues.indexOf(shelf.value) === -1);
    }

    update() {
        this.checkboxList.update();

        const shelves = Storage.getDecoded('shelves');
        if (shelves !== null) {
            this.pager.update(shelves.prev_page, shelves.next_page);
        }
    }

    addEvents() {
        const backBtn = document.querySelector('#exclude-latest-book-shelves-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));

        const selectShelfBtn = document.querySelector('#exclude-shelfs-btn');
        selectShelfBtn.addEventListener('click', (event) => {
            this.selectExcludedShelvesBtnListener(event);
        });
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('exclude-latest-book-shelves-back');
    }

    selectExcludedShelvesBtnListener(event) {
        event.preventDefault();

        this.emit('exclude-latest-book-shelves-next');
    }

    onPaginate(page) {
        const profile = Storage.getDecoded('profile');
        this.emit(
            'exclude-latest-book-shelves-request',
            { name: profile.name, value: profile.value, page: page },
        )
    }
}