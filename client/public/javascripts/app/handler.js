import Storage from './storage.js';
import {EventEmitter} from '../mixin/event_emitter.js';


class Handler {
    constructor(transport) {
        this.transport = transport;

        this.transport.onmessage((event) => this.handle(event));

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

        if (this.handlers.hasOwnProperty(operation)) {
            this.handlers[operation].forEach(handler => handler(message))
        } else {
            console.error(`Handler for operation ${operation} not defined.`)
        }
    }

    registerHandlers() {
        this.register('shelves', (message) => {
            if (message.payload.items.length !== 0) {
                Storage.setEncoded('shelves', message.payload);
            } else {
                Storage.remove('shelves');
            }

            this.emit(`shelves-results`);
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

            this.emit('search-profile-results');
        });

        this.register("search-latest-books", (message) => {
            if (message.payload.result) {
                Storage.setEncoded('latestBooks', message.payload.result);
            } else {
                Storage.remove('latestBooks');
            }

            this.emit('search-latest-books-results');
        });
    }
}


Object.assign(Handler.prototype, EventEmitter);

export default Handler;
