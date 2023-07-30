"use strict";

import Field from '../widgets/field.js';
import Storage from '../app/storage.js';
import RadioList from '../widgets/radio_list.js';
import LoadingBtn from '../widgets/loading_btn.js';
import Pager from '../widgets/pager.js';
import { InternalServerError } from '../app/exception.js';


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
        super(transport);

        this.on('confirm-profile-paginate', page => this.onPaginate(page));

        this.on('confirm-profile', () => this.onConfirmProfile());
    }

    static toString() { return 'confirm-profile' }

    onInit() {
        if (Storage.get('profiles') !== null) {
            super.onInit();
        } else {
            this.emit('no-profile-init');
        }
    }

    onRender() {
        this.radioList = new RadioList('profiles', 'profile');

        this.pager = new Pager('profile-list-container', 'confirm-profile-paginate');

        this.loadingBtn = new LoadingBtn('#confirm-profile-btn');

        this.addEvents();
        this.update();
    }

    onConfirmProfile() {
        const profile = this.radioList.checked;

        this.transport.post('profile', profile)
            .then(response => {
                if (!response.ok) {
                    throw new InternalServerError(response.status);
                } else {
                    return Promise.resolve();
                }
            })
            .then(() => this.emit('confirm-profile-next'))
            .catch(error => console.error(error));
    }

    onNext() {
        Storage.setEncoded('profile', this.radioList.checked);
        Storage.remove('profiles', 'searchProfile');

        this.emit('confirm-profile-hide');
        this.emit('catalogs-init');
    }

    onHide() {
        this.loadingBtn.hide();
        super.onHide();
     }

    onBack() {
        Storage.remove('profile', 'profiles');

        this.emit('confirm-profile-hide');
        this.emit('search-profile-init');
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
        this.emit('confirm-profile-init', {phrase: profile, page: page});
    }

    confirmBtnListener(event) {
        event.preventDefault();

        this.loadingBtn.show();

        this.emit('confirm-profile');
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('confirm-profile-back');
    }
}


export default ConfirmProfile;
