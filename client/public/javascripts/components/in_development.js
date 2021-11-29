import Field from './widgets/field.js';


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
          Start
        </button>
      </fieldset>
    `;

    constructor(transport) {
        super();

        this.transport = transport;
    }

    static toString() { return 'in-development' }

    onRender() {
        this.addEvents();
    }

    onBack() {
        this.emit('in-development-hide');
        this.emit(`start-page-request`);
    }

    addEvents() {
        const backBtn = document.querySelector('#in-development-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('in-development-back');
    }
}


export default InDevelopment;
