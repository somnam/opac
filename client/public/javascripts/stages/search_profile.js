import Field from '../widgets/field.js';
import Storage from '../storage.js';


class SearchProfile extends Field {
    template = `
        <template>
          <fieldset id="search-profile-fields">
            <div id="search-profile-container" class="nes-container with-title mb-4">
              <h3 class="title">Profile name</h3>
              <p class="input-hint">
              Can be found on your account page by the profile picture.
              </p>
              <input class="nes-input" id="profile-name" required="" />
            </div>

            <button class="nes-btn is-disabled btn-block mb-4" id="search-profile-btn">
              Next
            </button>

            <button class="nes-btn btn-block mb-4" id="go-back-btn">
              Back
            </button>
          </fieldset>
        </template>
    `;

    constructor() {
        super();

        this.on('search-profile-show', () => this.onShow());

        this.on('search-profile-hide', () => this.remove());

        this.on('search-profile-results', () => this.emit('search-profile-hide'));
    }

    get caller() {
        const activity = Storage.getDecoded('activity');
        if (activity)
            return activity.caller;

        const activities = Storage.getDecoded('activities');
        if (activities.items.length !== 0)
            return activities.items[0].caller;

        return 'activities';
    }

    onShow() {
        this.render()
            .then(() => {
                this.addEvents();
                this.update();
            })
            .catch(error => console.error(error));
    }

    addEvents() {
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

        const backBtn = document.querySelector('#search-profile-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));
    }

    update() {
        const storedProfileName = Storage.get('searchProfile');
        if (storedProfileName !== null) {
            const profileName = document.querySelector('#profile-name');
            profileName.value = storedProfileName;

            const searchProfileBtn = document.querySelector('#search-profile-btn');
            searchProfileBtn.classList.remove('is-disabled');
            searchProfileBtn.classList.add('is-primary');
        }
    }

    profileNameListener(event) {
        const profileName = event.target.value;
        const searchProfileBtn = document.querySelector('#search-profile-btn');

        if (profileName.length === 0) {
            Storage.remove('searchProfile');
            searchProfileBtn.classList.remove('is-primary');
            searchProfileBtn.classList.add('is-disabled');
        } else {
            Storage.set('searchProfile', profileName);
            searchProfileBtn.classList.remove('is-disabled');
            searchProfileBtn.classList.add('is-primary');
        }
    }

    searchProfileBtnListener(event) {
        event.preventDefault();

        const profileName = document.querySelector('#profile-name').value;
        if (profileName.length === 0)
            return;

        Storage.set('searchProfile', profileName);

        this.showLoading('#search-profile-btn');

        this.emit('search-profile-request', {phrase: profileName});
    }

    backBtnListener(event) {
        event.preventDefault();

        Storage.remove('searchProfile');

        this.emit('search-profile-step-back', this.caller);
    }
}


export default SearchProfile;
