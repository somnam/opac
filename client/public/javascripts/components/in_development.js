import Field from './widgets/field.js';
import Storage from '../app/storage.js';


class InDevelopment extends Field {
    template = `
      <fieldset id="in-development-fields">
        <div id="in-development-container" class="nes-container with-title mb-4">
          <h3 class="title">Work in progress</h3>
          <p class="input-hint">
          Feature will be ready soon.
          </p>
        </div>

        <button class="nes-btn btn-block mb-4" id="go-back-btn">
          Back
        </button>
      </fieldset>
    `;

    constructor(transport) {
        super();

        this.transport = transport;

        this.on('in-development-show', (caller) => {
            this.caller = caller;
            this.onShow();
        });

        this.on('in-development-hide', () => this.remove());

        this.on('in-development-back', (caller) => {
            this.emit('in-development-hide');
            this.emit(`${caller}-show`);
        });
    }

    static toString() { return 'in-development' }

    onShow() {
        this.render()
            .then(() => this.addEvents())
            .catch(error => console.error(error));
    }

    addEvents() {
        const backBtn = document.querySelector('#in-development-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('in-development-back', this.caller);
    }
}


export default InDevelopment;
