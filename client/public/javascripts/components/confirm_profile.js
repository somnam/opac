import Field from './widgets/field.js';
import Storage from '../app/storage.js';
import RadioList from './widgets/radio_list.js';
import LoadingBtn from './widgets/loading_btn.js';
import Pager from './widgets/pager.js';


class ConfirmProfile extends Field {
    template = `
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
    `;

    constructor(transport) {
        super();

        this.transport = transport;

        this.on('confirm-profile-show', () => this.onShow());

        this.on('confirm-profile-hide', () => this.remove());

        this.on('confirm-profile-paginate', page => this.onPaginate(page));

        this.on('confirm-profile-next', () => this.onNext());

        this.on('confirm-profile-back', () => this.onBack());

        this.on('post-profile', (profile) => this.onPostProfile(profile));
    }

    static toString() { return 'confirm-profile' }

    onShow() {
        this.render()
            .then(() => {
                this.radioList = new RadioList('profiles', 'profile');

                this.pager = new Pager('profile-list-container', 'confirm-profile-paginate');

                this.loadingBtn = new LoadingBtn('#confirm-profile-btn');

                this.addEvents();
                this.update();
            })
            .catch(error => console.error(error));
    }

    onNext() {
        const profile = this.radioList.checked;

        Storage.setEncoded('profile', profile);

        this.emit('post-profile', profile);

        const activity = Storage.getDecoded('activity');

        switch(activity ? activity.value : null) {
            case 'search-books':
                this.emit('shelves-request', profile);
                break;
            case 'search-latest-books':
                this.emit('include-latest-book-shelves-request', profile);
                break;
            default:
                console.error("No activity defined.");
                break;
        }
    }

    onPostProfile(profile) {
        this.transport.send('post-profile', profile);
    }

    onBack() {
        Storage.remove('profile', 'profiles');

        this.emit('confirm-profile-hide');
        this.emit('search-profile-show');
    }

    update() {
        this.radioList.update();

        const profiles = Storage.getDecoded('profiles');
        if (profiles !== null) {
            this.pager.update(profiles.prev_page, profiles.next_page);
        }
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

        this.loadingBtn.show();

        this.emit('confirm-profile-next');
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('confirm-profile-back');
    }
}


export default ConfirmProfile;
