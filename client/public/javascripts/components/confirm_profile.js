import Field from './widgets/field.js';
import Storage from '../app/storage.js';
import RadioList from './widgets/radio_list.js';
import Pager from './widgets/pager.js';


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

    constructor(transport) {
        super();

        this.transport = transport;

        this.radioList = new RadioList('profiles', 'profile');

        this.pager = new Pager('profile-list-container', 'confirm-profile-paginate');

        this.on('confirm-profile-show', () => this.onShow());

        this.on('confirm-profile-hide', () => this.remove());

        this.on('confirm-profile-paginate', (page) => this.onPaginate(page));

        this.on('confirm-profile-next', (profile) => this.onNext(profile));

        this.on('confirm-profile-step-back', () => {
            this.emit('confirm-profile-hide');
            this.emit('search-profile-show');
        });
    }

    static toString() { return 'confirm-profile' }

    onShow() {
        this.render()
            .then(() => {
                this.addEvents();
                this.update();
            })
            .catch(error => console.error(error));
    }

    onNext(profile) {

        const activity = Storage.getDecoded('activity');

        switch(activity ? activity.value : null) {
            case 'search-books':
                this.emit('shelves-request', profile)
                break;
            case 'search-latest-books':
                this.emit('confirm-profile-hide');
                this.emit('search-latest-books-request', {
                    "catalog": Storage.getDecoded('catalog'),
                    "profile": Storage.getDecoded('profile'),
                });
                break;
            default:
                console.error("No activity defined.");
                break;
        }
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

        this.emit('confirm-profile-next', profile)
    }

    backBtnListener(event) {
        event.preventDefault();

        Storage.remove('profile', 'profiles');

        this.emit('confirm-profile-step-back');
    }
}


export default ConfirmProfile;
