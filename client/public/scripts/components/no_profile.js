"use strict";

import Field from '../widgets/field.js';


class NoProfile extends Field {
    template = `
      <fieldset id="no-profile-fields">
        <div id="no-profile-container" class="nes-container with-title mb-4">
          <h3 class="title">Profile not found</h3>
          <p class="input-hint">
          Profile with the given name was not found. Try another?
          </p>
        </div>

        <button class="nes-btn btn-block mb-4" id="go-back-btn">
          Back
        </button>
      </fieldset>
    `;

    static toString() { return 'no-profile' }

    onRender() {
      this.addEvents();
    }

    onBack() {
        this.emit('no-profile-hide');
        this.emit('search-profile-init');
    }

    addEvents() {
        const backBtn = document.querySelector('#no-profile-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('no-profile-back');
    }
}


export default NoProfile;
