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

        this.on('libraries-request', (page) => {
            this.ws.send("libraries", {page: page});
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

        this.ws.on("libraries", (message) => {
            const libraries = message.payload.libraries;

            if (libraries.length !== 0) {
                this.storage.setItem('libraries', JSON.stringify(libraries));
            } else {
                this.storage.removeItem('libraries');
            }

            this.emit('libraries-results');
        });
    }
}


Object.assign(Adapter.prototype, EventEmitter);

export default Adapter;
