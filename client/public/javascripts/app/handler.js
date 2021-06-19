import Storage from './storage.js';
import {EventEmitter} from '../mixin/event_emitter.js';


class Handler {
    requests = ['search-profile', 'shelves']
    responses = ['shelves']

    constructor(transport) {
        this.transport = transport;
        this.transport.onmessage((event) => this.handle(event));

        this.handlers = {};

        this.setRequestRoutes();
        this.setResponseRoutes();
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

    setRequestRoutes() {
        this.requests.forEach((resource) => {
            this.on(`${resource}-request`, (message) => {
                this.transport.send(resource, message);
            });
        });
    }

    setResponseRoutes() {
        this.responses.forEach((resource) => {
            this.register(resource, (message) => {
                if (message.payload.items.length !== 0) {
                    Storage.setEncoded(resource, message.payload);
                } else {
                    Storage.remove(resource);
                }

                this.emit(`${resource}-results`);
            });
        });

        this.register("search-profile", (message) => {
            if (message.payload.items.length !== 0) {
                Storage.setEncoded('profiles', message.payload);
            } else {
                Storage.remove('profiles');
            }

            this.emit('search-profile-results');
        });
    }
}


Object.assign(Handler.prototype, EventEmitter);

export default Handler;
