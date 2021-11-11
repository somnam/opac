import Storage from './storage.js';
import {EventEmitter} from '../mixin/event_emitter.js';


class Handler {
    constructor() {
        this.handlers = {};

        this.registerHandlers();
    }

    register(operation, handler) {
        this.handlers[operation] = this.handlers[operation] || [];
        this.handlers[operation].push(handler);
    }

    handle(event) {
        const message = JSON.parse(event.data),
              operation = message.operation;

        return new Promise((resolve, reject) => {
            if (this.handlers.hasOwnProperty(operation)) {
                this.handlers[operation].forEach(handler => handler(message));
                resolve();
            } else {
                reject(`Handler for operation ${operation} not defined.`);
            }
        });
    }

    registerHandlers() {
        this.register('shelves', (message) => {
            if (message.payload.items.length !== 0) {
                Storage.setEncoded('shelves', message.payload);
            } else {
                Storage.remove('shelves');
            }
        });

        this.register("open-connection", (message) => {
            if (message.payload.client_id) {
                Storage.set("clientId", message.payload.client_id);
            }
        });

        this.register("search-profile", (message) => {
            if (message.payload.items.length !== 0) {
                Storage.setEncoded('profiles', message.payload);
            } else {
                Storage.remove('profiles');
            }
        });
    }
}


Object.assign(Handler.prototype, EventEmitter);

export default Handler;
