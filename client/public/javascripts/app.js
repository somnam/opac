import Transport from './transport.js';
import Broker from './broker.js';
import State from './state.js';
import Stages from './stages.js';


class WebSocketApp {
    constructor() {
        (new Transport())
            .then(transport => {
                this.broker = new Broker(transport);
                this.stages = new Stages();
                this.state = new State();

                this.state.restore();
            })
            .catch(error => console.error(error));
    }
}


document.addEventListener("DOMContentLoaded", () => new WebSocketApp());
