import Field from './widgets/field.js';
import Storage from '../app/storage.js';


class SearchLatestBooks extends Field {
    constructor(transport) {
        super();
    }

    static toString() { return 'search-latest-books' }

    onRequest() {
        const catalog = Storage.getDecoded('catalog');

        switch(catalog ? catalog.value : null) {
            case "4949":
                this.emit('activities-hide');
                this.emit('in-development-request');
                break;
            case "5004":
                const profile = Storage.getDecoded('profile');
                this.emit('activities-hide');
                this.emit('include-latest-book-shelves-request', profile);
                break;
            default:
                console.error("No catalog defined.");
                break;
        }
    }
}


export default SearchLatestBooks;