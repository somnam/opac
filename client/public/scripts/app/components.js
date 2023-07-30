"use strict";

import Start from '../components/start.js';
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
    constructor(transport, state) {
        this.components = [];

        [
            Start,
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
        ].forEach((componentClass) => {
            const component = new componentClass(transport);
            component.on(`${component}-init`, () => {
                state.current = `${component}`;
            });
            this.components.push(component);
        });
    }
}


export default Components;
