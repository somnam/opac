import Field from './widgets/field.js';
import Storage from '../app/storage.js';
import CheckboxList from './widgets/checkbox_list.js';
import Pager from './widgets/pager.js';


export default class IncludeLatestBooksShelves extends Field {
    template = `
    <fieldset id="include-latest-book-shelves-fields">
        <div id="shelf-list-container" class="nes-container with-title mb-4">
            <h3 class="title">Include shelves</h3>
            <div class="item" id="include-latest-book-shelves-list"></div>
        </div>

        <button class="nes-btn is-primary btn-block mb-4" id="include-shelfs-btn">
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

        this.on('include-latest-book-shelves-show', () => this.onShow());

        this.on('include-latest-book-shelves-hide', () => this.remove());

        this.on('include-latest-book-shelves-paginate', page => this.onPaginate(page));

        this.on(`include-latest-book-shelves-request`, message => this.onRequest(message));

        this.on(`include-latest-book-shelves-data`, () => this.onData());

        this.on('include-latest-book-shelves-next', () => this.onNext());

        this.on('include-latest-book-shelves-back', () => this.onBack());
    }

    static toString() { return 'include-latest-book-shelves' }

    onRequest(message) {
        this.transport.fetch('shelves', message)
            .then(() => this.emit('include-latest-book-shelves-data'))
            .catch(error => console.error(error));
    }

    onData() {
        this.emit('confirm-profile-hide');
        this.emit('include-latest-book-shelves-show');
    }

    onShow() {
        this.render()
            .then(() => {
                this.checkboxList = new CheckboxList('shelves', 'include-latest-book-shelves');

                this.pager = new Pager(
                    'shelf-list-container',
                    'include-latest-book-shelves-paginate',
                );

                this.addEvents();
                this.update();
            })
            .catch(error => console.error(error));
    }

    onNext() {
        const shelves = this.checkboxList.checked;
        const profile = Storage.getDecoded('profile');

        Storage.setEncoded('include-latest-book-shelves', shelves);

        this.emit('exclude-latest-book-shelves-request', profile);
    }

    onBack() {
        Storage.remove('include-latest-book-shelves', 'shelves');

        this.emit('include-latest-book-shelves-hide');
        this.emit('confirm-profile-show');
    }

    update() {
        this.checkboxList.update();

        const shelves = Storage.getDecoded('shelves');
        if (shelves !== null) {
            this.pager.update(shelves.prev_page, shelves.next_page);
        }
    }

    addEvents() {
        const backBtn = document.querySelector('#include-latest-book-shelves-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));

        const selectShelfBtn = document.querySelector('#include-shelfs-btn');
        selectShelfBtn.addEventListener('click', event => this.selectIncludedShelvesBtnListener(event));
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('include-latest-book-shelves-back');
    }

    selectIncludedShelvesBtnListener(event) {
        event.preventDefault();

        this.emit('include-latest-book-shelves-next');
    }

    onPaginate(page) {
        const profile = Storage.getDecoded('profile');

        this.emit(
            'include-latest-book-shelves-request',
            { name: profile.name, value: profile.value, page: page },
        )
    }
}