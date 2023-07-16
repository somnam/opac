import StartPage from '../components/start_page.js';
import Activities from '../components/activities.js';
import Catalogs from '../components/catalogs.js';
import ConfirmProfile from '../components/confirm_profile.js';
import InDevelopment from '../components/in_development.js';
import NoProfile from '../components/no_profile.js';
import SearchCatalog from '../components/search_catalog.js';
import SearchLatestBooks from '../components/search_latest_books.js';
import LatestBooks from '../components/latest_books.js';
import IncludeLatestBooksShelves from '../components/include_latest_books_shelves.js';
import ExcludeLatestBooksShelves from '../components/exclude_latest_books_shelves.js';
import SearchProfile from '../components/search_profile.js';
import Shelves from '../components/shelves.js';


class Components {
    constructor(transport) {
        this.components = [];

        [
            StartPage,
            Activities,
            Catalogs,
            ConfirmProfile,
            InDevelopment,
            NoProfile,
            SearchCatalog,
            SearchLatestBooks,
            LatestBooks,
            IncludeLatestBooksShelves,
            ExcludeLatestBooksShelves,
            SearchProfile,
            Shelves,
        ].forEach((component) => {
            this.components.push(new component(transport));
        });
    }
}


export default Components;
