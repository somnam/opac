import {EventEmitter} from '../mixin/event_emitter.js';


class SearchCatalog {
    constructor(transport) {
        this.transport = transport;

        this.on('search-catalog-request', () => this.onRequest());
    }

    onRequest() {
        this.emit('shelves-hide');
        this.emit('in-development-show');
    }
}


Object.assign(SearchCatalog.prototype, EventEmitter);


export default SearchCatalog;
