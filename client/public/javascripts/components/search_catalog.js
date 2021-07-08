import {EventEmitter} from '../mixin/event_emitter.js';


class SearchCatalog {
    constructor(transport) {
        this.transport = transport;

        this.on('search-catalog-request', () => {
            this.emit('shelves-hide');
            this.emit('in-development-show', 'shelves');
        });
    }
}


Object.assign(SearchCatalog.prototype, EventEmitter);


export default SearchCatalog;
