import Storage from './storage.js';
import {EventEmitter} from '../mixin/event_emitter.js';
import Catalogs from '../components/catalogs.js';
import Activities from '../components/activities.js';
import SearchProfile from '../components/search_profile.js';
import NoProfile from '../components/no_profile.js';
import ConfirmProfile from '../components/confirm_profile.js';
import Shelves from '../components/shelves.js';
import InDevelopment from '../components/in_development.js';
import SearchLatestBooks from '../components/search_latest_books.js';
import IncludeLatestBooksShelves from '../components/include_latest_books_shelves.js';
import ExcludeeLatestBooksShelves from '../components/exclude_latest_books_shelves.js';


class State {
    constructor() {
        this.current = Storage.get('current') || 'catalogs';

        [
            Catalogs,
            Activities,
            SearchProfile,
            NoProfile,
            ConfirmProfile,
            Shelves,
            InDevelopment,
            SearchLatestBooks,
            IncludeLatestBooksShelves,
            ExcludeeLatestBooksShelves,
        ].forEach((component) =>{
            const componentName = component.toString();
            this.on(`${componentName}-show`, () => this.current = componentName);
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
        this.emit(`${this.current}-show`);
    }
}


Object.assign(State.prototype, EventEmitter);


export default State;
