import Field from '../widgets/field.js';
import Storage from '../storage.js';
import RadioList from '../widgets/radio_list.js';
import Pager from '../widgets/pager.js';


class ConfirmProfile extends Field {
    template = `
        <template>
          <fieldset id="confirm-profile-fields">
            <div id="profile-list-container" class="nes-container with-title mb-4">
              <h3 class="title">Is this you?</h3>
              <div class="item" id="profile-list">
              </div>
            </div>

            <button class="nes-btn is-primary btn-block mb-4" id="confirm-profile-btn">
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

        this.radioList = new RadioList('profiles', 'profile');

        this.pager = new Pager('profile-list-container', 'confirm-profile-paginate');

        this.on('confirm-profile-show', () => this.onShow());

        this.on('confirm-profile-hide', () => this.remove());

        this.on('confirm-profile-paginate', (page) => this.onPaginate(page));
    }

    onShow() {
        this.render()
            .then(() => {
                this.addEvents();
                this.update();
            })
            .catch(error => console.error(error));
    }

    update() {
        this.radioList.update();

        const profiles = Storage.getDecoded('profiles');
        if (profiles !== null)
            this.pager.update(profiles.prev_page, profiles.next_page);
    }

    addEvents() {
        const backBtn = document.querySelector('#confirm-profile-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));

        const confirmBtn = document.querySelector('#confirm-profile-btn');
        confirmBtn.addEventListener('click', (event) => this.confirmBtnListener(event));
    }

    onPaginate(page) {
        const profile = Storage.get('searchProfile');
        this.emit('search-profile-request', {phrase: profile, page: page});
    }

    confirmBtnListener(event) {
        event.preventDefault();

        const profile = this.radioList.checked;

        Storage.setEncoded('profile', profile);

        this.showLoading('#confirm-profile-btn');

        this.emit('shelves-request', {name: profile.name, value: profile.value})
    }

    backBtnListener(event) {
        event.preventDefault();

        Storage.remove('profile', 'profiles');

        this.emit('confirm-profile-step-back');
    }
}


export default ConfirmProfile;
