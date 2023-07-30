"use strict";

import Field from '../widgets/field.js';
import ButtonGroup from '../widgets/button_group.js';
import Storage from '../app/storage.js';
import { NotFoundError, InternalServerError } from '../app/exception.js';


class StartPage extends Field {
    template = `
      <fieldset id="start-fields">
        <h2 id="title" class="mb-4">Hello</h2>
        <div id="shelves-list-container" class="nes-container with-title mb-4">
            <h3 class="title">Shelves</h3>
            <div class="item mb-4" id="available-shelves-group">
            </div>
            <div class="item mb-4" id="pending-shelves-group">
            </div>
        </div>

        <button class="nes-btn is-primary btn-block mb-4" id="catalogs-btn">
          To Catalogs
        </button>

        <button class="nes-btn btn-block mb-4" id="switch-profile-btn">
          Change Profile
        </button>

       </fieldset>
    `;

    static toString() { return 'start' }

    onInit() {
        if (!Storage.get('profile')) {
            this.emit('search-profile-init');
            return;
        }

        const profile = Storage.getDecoded('profile');

        this.transport.get(`profile/${profile.uuid}/shelves`)
            .then(response => {
                if (response.status === 404) {
                    throw new NotFoundError();
                }
                if (!response.ok) {
                    throw new InternalServerError(response.status);
                } else {
                    return response.json();
                }
            })
            .then(result => {
                Storage.setEncoded('shelves', result);
                super.onInit();
            })
            .catch(error => {
                if (error.code && error.code === 404) {
                    this.emit('search-profile-init');
                } else {
                    console.error(error);
                }
            });
    }

    onRender() {
        this.availableShelves = new ButtonGroup('available-shelves', 'is-success');

        this.pendingShelves = new ButtonGroup('pending-shelves', 'is-warning');

        this.addEvents();

        this.update();
    }

    update() {
        this.updateTitle();

        const shelves = Storage.getDecoded('shelves');

        this.availableShelves.update(shelves.items.filter(shelf => !!shelf.refreshed_at));

        this.pendingShelves.update(shelves.items.filter(shelf => !shelf.refreshed_at));
    }

    updateTitle() {
        if (!Storage.get('profile')) {
            return;
        }

        const profile = Storage.getDecoded('profile');

        const title = document.querySelector('h2[id="title"]');

        title.innerHTML = `${title.innerHTML} ${profile.name}`;
    }

    addEvents() {
        const catalogsBtn = document.querySelector('#catalogs-btn');
        catalogsBtn.addEventListener('click', (event) => {
            this.catalogsBtnEventListener(event);
        });

        const switchProfileBtn = document.querySelector('#switch-profile-btn');
        switchProfileBtn.addEventListener('click', (event) => {
            this.switchProfileBtnEventListener(event);
        });
    }

    catalogsBtnEventListener(event) {
        event.preventDefault();
        this.emit(`${this}-next`);
    }

    switchProfileBtnEventListener(event) {
        event.preventDefault();

        Storage.remove('shelves');

        this.emit(`search-profile-init`);
    }

    onNext() {
        this.emit(`${this}-hide`);
        this.emit('catalogs-init');
    }

}

export default StartPage;
