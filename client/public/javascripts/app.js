import Transport from './app/transport.js';
import Handler from './app/handler.js';
import Components from './app/components.js';
import State from './app/state.js';


class WebSocketApp {
    constructor() {
        (new Transport())
            .then(transport => {
                this.handler = new Handler(transport);
                this.components = new Components(transport);
                this.state = new State();

                this.state.restore();
            })
            .catch(error => console.error(error));
    }
}


document.addEventListener("DOMContentLoaded", () => new WebSocketApp());
