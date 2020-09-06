import {FieldMixin} from '../mixin/field.js';
import {EventEmitter} from '../mixin/event_emitter.js';
import {RadioList, RadioListParams} from '../widgets/radio_list.js';
import {Pager, PagerParams} from '../widgets/pager.js';


class Shelves {
    constructor() {
        this.radio_list = new RadioList('shelf-list-container', 'shelf');

        this.pager = new Pager('shelf-list-container', 'shelves-paginate');

        this.on('shelves-show', () => this.onShelvesShow());

        // this.on('shelves-hide', () => );
        this.on('shelves-hide', () => this.onShelvesHide());

        this.on('shelves-results', () => this.emit('shelves-show'));

        this.on('shelves-paginate', (page) => this.onPaginate(page));

        this.on('catalogs-results', () => this.emit('shelves-hide'));
    }

    onDomLoaded() {
        const backBtn = document.querySelector('#shelves-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));

        const selectShelfBtn = document.querySelector('#select-shelf-btn');
        selectShelfBtn.addEventListener('click', (event) => {
            this.selectShelfBtnListener(event);
        });
    }

    onShelvesShow() {
        const shelvesResultsJson = this.storage.getItem('shelvesResults');
        if (shelvesResultsJson !== null) {
            const shelvesResults = JSON.parse(shelvesResultsJson);

            const shelfJson = this.storage.getItem('shelf');
            const shelf = shelfJson !== null ? JSON.parse(shelfJson) : null;

            this.radio_list.update(new RadioListParams(
                shelvesResults.items,
                shelf,
            ));

            this.pager.update(new PagerParams(
                shelvesResults.prevPage,
                shelvesResults.nextPage,
            ));
        }

        this.show('#shelves-fields');
    }

    onShelvesHide() {
        this.hide('#shelves-fields');
        this.hideLoading('#select-shelf-btn');
    }

    onPaginate(page) {
        const profile = JSON.parse(this.storage.getItem('profile'));
        this.emit('confirm-profile-send', profile, page);
    }

    backBtnListener(event) {
        event.preventDefault();

        this.storage.removeItem('shelf');
        this.storage.removeItem('shelvesResults');

        this.emit('shelves-hide');
        this.emit('confirm-profile-show');
    }

    selectShelfBtnListener(event) {
        event.preventDefault();

        const value = document.querySelector('input[name="shelf"]:checked').value;

        const shelvesResults = JSON.parse(this.storage.getItem('shelvesResults'));

        const shelfIndex = shelvesResults.items.findIndex((elem) => elem.value === value);

        const shelf = shelvesResults.items[shelfIndex];

        this.storage.setItem('shelf', JSON.stringify(shelf));

        this.showLoading('#select-shelf-btn');

        this.emit('catalogs-request');
    }
}


Object.assign(Shelves.prototype, EventEmitter);
Object.assign(Shelves.prototype, FieldMixin);


export default Shelves;
