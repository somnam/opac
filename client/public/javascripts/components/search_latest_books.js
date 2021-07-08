import Storage from '../app/storage.js';
import {EventEmitter} from '../mixin/event_emitter.js';


class SearchLatestBooks {
    constructor(transport) {
        this.transport = transport;

        this.on('search-latest-books-start', () => this.onStart());

        this.on(`search-latest-books-request`, (message) => {
            this.transport.send('search-latest-books', message);
        });
    }

    onStart() {
        const catalog = Storage.getDecoded('catalog');

        switch(catalog ? catalog.value : null) {
            case "4949":
                this.emit('activities-hide');
                this.emit('in-development-show', 'activities');
                break;
            case "5004":
                this.emit('activities-hide');
                this.emit('search-profile-show');
                break;
            default:
                console.error("No catalog defined.");
                break;
        }
    }
}


Object.assign(SearchLatestBooks.prototype, EventEmitter);


export default SearchLatestBooks;
