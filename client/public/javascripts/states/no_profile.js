import Field from '../widgets/field.js';
import Storage from '../app/storage.js';


class NoProfile extends Field {
    template = `
        <template>
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
        </template>
    `;

    constructor() {
        super();

        this.on('no-profile-show', () => this.onShow());

        this.on('no-profile-hide', () => this.remove());
    }

    toString() { return 'no-profile' }

    onShow(caller) {
        this.render()
            .then(() => this.addEvents())
            .catch(error => console.error(error));
    }

    addEvents() {
        const backBtn = document.querySelector('#no-profile-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('no-profile-step-back');
    }
}


export default NoProfile;
