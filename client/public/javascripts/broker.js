import Storage from './storage.js';
import {EventEmitter} from './mixin/event_emitter.js';


class Broker {
    requests = ['catalogs', 'activities', 'search-profile', 'shelves']
    responses = ['activities', 'shelves']

    constructor(transport) {
        this.transport = transport;

        this.setRequestRoutes();
        this.setResponseRoutes();
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
            this.transport.on(resource, (message) => {
                if (message.payload.items.length !== 0) {
                    Storage.setEncoded(resource, message.payload);
                } else {
                    Storage.remove(resource);
                }

                this.emit(`${resource}-results`);
            });
        });

        this.transport.on("catalogs", (message) => {
            message.payload.items = message.payload.items.map(
                (catalog) => {
                    return {
                        name: `${catalog.name} (${catalog.city})`,
                        value: catalog.value
                    }
                }
            )

            if (message.payload.items.length !== 0) {
                Storage.setEncoded('catalogs', message.payload);
            } else {
                Storage.remove('catalogs');
            }

            this.emit('catalogs-results');
        });

        this.transport.on("search-profile", (message) => {
            if (message.payload.items.length !== 0) {
                Storage.setEncoded('profiles', message.payload);
            } else {
                Storage.remove('profiles');
            }

            this.emit('search-profile-results');
        });
    }
}


Object.assign(Broker.prototype, EventEmitter);

export default Broker;
