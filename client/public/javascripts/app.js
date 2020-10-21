import Transport from './app/transport.js';
import Broker from './app/broker.js';
import State from './app/state.js';
import Stages from './app/stages.js';


class WebSocketApp {
    constructor() {
        (new Transport())
            .then(transport => {
                this.broker = new Broker(transport);
                this.state = new State();
                this.stages = new Stages();

                this.state.restore();
            })
            .catch(error => console.error(error));
    }
}


document.addEventListener("DOMContentLoaded", () => new WebSocketApp());
