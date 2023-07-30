"use strict";

import Transport from './app/transport.js';
import Components from './app/components.js';
import Start from './components/start.js';
import State from './app/state.js';


class App {
    constructor() {
        (new Transport('localhost', '8888', false))
            .then(transport => {
                this.transport = transport;
                this.state = new State(Start.toString());
                this.components = new Components(this.transport, this.state);

                this.state.restore();
            })
            .catch(error => console.error(error));
    }
}


document.addEventListener("DOMContentLoaded", () => new App());
