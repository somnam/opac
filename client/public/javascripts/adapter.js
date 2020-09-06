import WS from './ws.js';
import {EventEmitter} from './mixin/event_emitter.js';


class Adapter {
    storage = localStorage
    ws = new WS()

    constructor() {
        this.on('search-profile-send', (profileName, page) => {
            this.ws.send(
                "search_profile",
                {phrase: profileName, page: page}
            );
        });

        this.on('confirm-profile-send', (profile, page) => {
            this.ws.send(
                "shelves",
                {name: profile.name, value: profile.value, page: page},
            );
        });

        this.on('catalogs-request', (page) => {
            this.ws.send("catalogs", {page: page});
        });

        this.ws.on("search_profile", (message) => {
            if (message.payload.items.length !== 0) {
                this.storage.setItem(
                    'profileResults',
                    JSON.stringify(message.payload),
                );
            } else {
                this.storage.removeItem('profileResults');
            }

            this.emit('search-profile-results');
        });

        this.ws.on("shelves", (message) => {
            if (message.payload.items.length !== 0) {
                this.storage.setItem(
                    'shelvesResults',
                    JSON.stringify(message.payload),
                );
            } else {
                this.storage.removeItem('shelvesResults');
            }

            this.emit('shelves-results');
        });

        this.ws.on("catalogs", (message) => {
            const catalogs = message.payload.catalogs.map(
                (catalog) => {
                    return {
                        name: `${catalog.name} (${catalog.city})`,
                        value: catalog.value
                    }
                }
            )

            if (catalogs.length !== 0) {
                this.storage.setItem('catalogs', JSON.stringify(catalogs));
            } else {
                this.storage.removeItem('catalogs');
            }

            this.emit('catalogs-results');
        });
    }
}


Object.assign(Adapter.prototype, EventEmitter);

export default Adapter;
