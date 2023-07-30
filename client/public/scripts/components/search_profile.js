"use strict";

import Field from '../widgets/field.js';
import Storage from '../app/storage.js';
import LoadingBtn from '../widgets/loading_btn.js';
import { InternalServerError } from '../app/exception.js';


class SearchProfile extends Field {
    template = `
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

        <button class="nes-btn is-disabled btn-block mb-4" hidden="hidden" id="go-back-btn">
            Back
        </button>
       </fieldset>
    `;

    static toString() { return 'search-profile' }

    onRender() {
        this.loadingBtn = new LoadingBtn('#search-profile-btn');

        this.addEvents();

        this.update();
    }

    onNext() {
        const profileName = document.querySelector('#profile-name').value;
        if (profileName.length === 0) {
            return;
        }
        Storage.set('searchProfile', profileName);

        this.transport.post('profile/search', {phrase: profileName})
            .then(response => {
                if (!response.ok) {
                    throw new InternalServerError(response.status);
                } else {
                    return response.json();
                }
            })
            .then(result => {
                this.emit('search-profile-hide');

                if (result.items.length !== 0) {
                    Storage.setEncoded('profiles', result);
                    this.emit('confirm-profile-init');
                } else {
                    this.emit('no-profile-init');
                }
            })
            .catch(error => console.error(error));

    }

    onBack() {
        this.emit('search-profile-hide');
        this.emit('start-init');
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

        const hasProfile = !!Storage.get('profile');
        if (hasProfile) {
            const backBtn = document.querySelector('#go-back-btn');
            backBtn.classList.remove('is-disabled');
            backBtn.removeAttribute('hidden');
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

        this.loadingBtn.show();

        this.emit('search-profile-next');
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('search-profile-back');
    }
}


export default SearchProfile;
