"use strict";

import Field from '../widgets/field.js';


class SearchCatalog extends Field {
    static toString() { return 'search-catalog' }

    onInit(message) {
        this.emit('shelves-hide');
        this.emit('in-development-init');
    }
}


export default SearchCatalog;
