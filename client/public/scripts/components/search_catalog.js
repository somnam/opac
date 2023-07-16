import Field from './widgets/field.js';


class SearchCatalog extends Field {
    constructor(transport) {
        super();

        this.transport = transport;
    }

    static toString() { return 'search-catalog' }

    onInit(message) {
        this.emit('shelves-hide');
        this.emit('in-development-init');
    }
}


export default SearchCatalog;
