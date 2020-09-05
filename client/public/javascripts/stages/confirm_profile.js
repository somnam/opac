import {FieldMixin} from '../mixin/field.js';
import {EventEmitter} from '../mixin/event_emitter.js';
import {RadioList, RadioListParams} from '../widgets/radio_list.js';
import {Pager, PagerParams} from '../widgets/pager.js';


class ConfirmProfile {
    constructor() {
        this.radio_list = new RadioList('profile-list-container', 'profile');

        this.pager = new Pager('profile-list-container', 'confirm-profile-paginate');

        this.on('confirm-profile-show', () => this.onProfileShow());

        this.on('confirm-profile-hide', () => this.onProfileHide());

        this.on('search-profile-results', () => this.emit('confirm-profile-show'));

        this.on('confirm-profile-paginate', (page) => this.onPaginate(page));

        this.on('shelves-results', () => this.emit('confirm-profile-hide'));
    }

    onDomLoaded() {
        const backBtn = document.querySelector('#confirm-profile-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));

        const confirmBtn = document.querySelector('#confirm-profile-btn');
        confirmBtn.addEventListener('click', (event) => this.confirmBtnListener(event));
    }

    onProfileShow() {
        const profileResultsJson = this.storage.getItem('profileResults');
        if (profileResultsJson !== null) {
            const profileResults = JSON.parse(profileResultsJson);

            const profileJson = this.storage.getItem('profile');
            const profile = profileJson !== null ? JSON.parse(profileJson) : null;

            this.radio_list.update(new RadioListParams(
                profileResults.items,
                profile,
            ));

            this.pager.update(new PagerParams(
                profileResults.prevPage,
                profileResults.nextPage,
            ));
        }

        this.show('#confirm-profile-fields');
    }

    onProfileHide() {
        this.hide('#confirm-profile-fields');
        this.hideLoading('#confirm-profile-btn');
    }

    onPaginate(page) {
        const profile = this.storage.getItem('searchProfile');
        this.emit('search-profile-send', profile, page);
    }

    backBtnListener(event) {
        event.preventDefault();

        this.storage.removeItem('profile');
        this.storage.removeItem('profileResults');

        this.emit('confirm-profile-hide');
        this.emit('search-profile-show');
    }

    confirmBtnListener(event) {
        event.preventDefault();

        const value = document.querySelector('input[name="profile"]:checked').value;

        const profileResults = JSON.parse(this.storage.getItem('profileResults'));

        const profileIndex = profileResults.items.findIndex((elem) => elem.value === value);

        const profile = profileResults.items[profileIndex];

        this.storage.setItem('profile', JSON.stringify(profile));

        this.showLoading('#confirm-profile-btn');

        this.emit('confirm-profile-send', profile);
    }
}


Object.assign(ConfirmProfile.prototype, EventEmitter);
Object.assign(ConfirmProfile.prototype, FieldMixin);


export default ConfirmProfile;
