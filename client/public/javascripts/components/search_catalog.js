import Field from './widgets/field.js';


class SearchCatalog extends Field {
    constructor(transport) {
        super();

        this.transport = transport;
    }

    static toString() { return 'search-catalog' }

    onRequest(message) {
        this.emit('shelves-hide');
        this.emit('in-development-request');
    }
}


export default SearchCatalog;
