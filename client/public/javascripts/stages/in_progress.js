import Field from '../widgets/field.js';
import Storage from '../storage.js';


class InProgress extends Field {
    template = `
        <template>
          <fieldset id="in-progress-fields">
            <div id="in-progress-container" class="nes-container with-title mb-4">
              <h3 class="title">Work in progress</h3>
              <p class="input-hint">
              Feature will be ready soon.
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

        this.on('in-progress-show', (caller) => {
            this.caller = caller;
            this.onShow();
        });

        this.on('in-progress-hide', () => this.remove());
    }

    onShow() {
        this.render()
            .then(() => this.addEvents())
            .catch(error => console.error(error));
    }

    addEvents() {
        const backBtn = document.querySelector('#in-progress-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('in-progress-hide');
        this.emit(`${this.caller}-show`);
    }
}


export default InProgress;
