import {FieldMixin} from '../mixin/field.js';
import {EventEmitter} from '../mixin/event_emitter.js';


class SearchProfile {
    constructor() {
        this.on('search-profile-show', () => this.onSearchShow());

        this.on('search-profile-hide', () => this.onSearchHide());

        this.on('search-profile-results', () => this.emit('search-profile-hide'));
    }

    onDomLoaded() {
        const profileName = document.querySelector('#profile-name');
        ['input', 'change', 'paste'].forEach((eventType) => {
            profileName.addEventListener(eventType, (event) => {
                this.profileNameListener(event);
            });
        });

        const searchProfileBtn = document.querySelector('#search-profile-btn');
        searchProfileBtn.addEventListener('click', (event) => {
            this.searchProfileBtnListener(event);
        });
    }

    onSearchShow() {
        const storedProfileName = this.storage.getItem('searchProfile');
        if (storedProfileName !== null) {
            const profileName = document.querySelector('#profile-name');
            profileName.value = storedProfileName;

            const searchProfileBtn = document.querySelector('#search-profile-btn');
            searchProfileBtn.classList.remove('is-disabled');
            searchProfileBtn.classList.add('is-primary');
        }

        this.show('#search-profile-fields');
    }

    onSearchHide() {
        this.hide('#search-profile-fields');
        this.hideLoading('#search-profile-btn');
    }

    profileNameListener(event) {
        const profileName = event.target.value;
        const searchProfileBtn = document.querySelector('#search-profile-btn');

        if (profileName.length === 0) {
            this.storage.removeItem('searchProfile');
            searchProfileBtn.classList.remove('is-primary');
            searchProfileBtn.classList.add('is-disabled');
        } else {
            this.storage.setItem('searchProfile', profileName);
            searchProfileBtn.classList.remove('is-disabled');
            searchProfileBtn.classList.add('is-primary');
        }
    }

    searchProfileBtnListener(event) {
        event.preventDefault();

        const profileName = document.querySelector('#profile-name').value;
        if (profileName.length === 0)
            return;

        this.storage.setItem('searchProfile', profileName);

        this.showLoading('#search-profile-btn');

        this.emit('search-profile-send', profileName);
    }
}


Object.assign(SearchProfile.prototype, EventEmitter);
Object.assign(SearchProfile.prototype, FieldMixin);


export default SearchProfile;
