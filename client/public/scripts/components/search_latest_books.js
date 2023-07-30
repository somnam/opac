"use strict";

import Field from '../widgets/field.js';
import Storage from '../app/storage.js';


class SearchLatestBooks extends Field {
    constructor(transport) {
        super();
    }

    static toString() { return 'search-latest-books' }

    onInit() {
        const catalog = Storage.getDecoded('catalog');

        switch(catalog ? catalog.value : null) {
            case "4949":
                this.emit('activities-hide');
                this.emit('in-development-init');
                break;
            case "5004":
                this.emit('activities-hide');
                this.emit('include-latest-book-shelves-init');
                break;
            default:
                console.error("No catalog defined.");
                break;
        }
    }
}


export default SearchLatestBooks;
