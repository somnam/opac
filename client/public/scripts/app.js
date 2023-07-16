import Transport from './app/transport.js';
import Components from './app/components.js';
import State from './app/state.js';


class App {
    constructor() {
        (new Transport('localhost', '8888', false))
            .then(transport => {
                this.state = new State();
                this.components = new Components(transport);

                this.state.restore();
            })
            .catch(error => console.error(error));
    }
}


document.addEventListener("DOMContentLoaded", () => new App());
