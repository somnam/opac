import Storage from './storage.js';
import {EventEmitter} from '../mixin/event_emitter.js';
import StartPage from '../components/start_page.js';
import Catalogs from '../components/catalogs.js';
import Activities from '../components/activities.js';
import SearchProfile from '../components/search_profile.js';
import NoProfile from '../components/no_profile.js';
import ConfirmProfile from '../components/confirm_profile.js';
import Shelves from '../components/shelves.js';
import InDevelopment from '../components/in_development.js';
import SearchLatestBooks from '../components/search_latest_books.js';
import LatestBooks from '../components/latest_books.js';
import IncludeLatestBooksShelves from '../components/include_latest_books_shelves.js';
import ExcludeeLatestBooksShelves from '../components/exclude_latest_books_shelves.js';


class State {

    constructor() {
        this.current = Storage.get('current') || 'start-page';

        [
            StartPage,
            Catalogs,
            Activities,
            SearchProfile,
            NoProfile,
            ConfirmProfile,
            Shelves,
            InDevelopment,
            SearchLatestBooks,
            LatestBooks,
            IncludeLatestBooksShelves,
            ExcludeeLatestBooksShelves,
        ].forEach((component) =>{
            this.on(`${component}-request`, () => this.current = `${component}`);
        });
    }

    get current() {
        return this._current;
    }

    set current(value) {
        this._current = value;
        Storage.set('current', value);
    }

    restore() {
        this.emit(`${this.current}-request`);
    }
}


Object.assign(State.prototype, EventEmitter);


export default State;
