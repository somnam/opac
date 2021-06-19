import Storage from './storage.js';
import {EventEmitter} from '../mixin/event_emitter.js';
import Catalogs from '../states/catalogs.js';
import Activities from '../states/activities.js';
import SearchProfile from '../states/search_profile.js';
import NoProfile from '../states/no_profile.js';
import ConfirmProfile from '../states/confirm_profile.js';
import Shelves from '../states/shelves.js';
import InProgress from '../states/in_progress.js';


class State {
    constructor() {
        this.current = Storage.get('current') || 'catalogs';

        this.available_states = [
            new Catalogs(),
            new Activities(),
            new SearchProfile(),
            new NoProfile(),
            new ConfirmProfile(),
            new Shelves(),
            new InProgress(),
        ];

        this.available_states.forEach((state) => {
            const stateName = state.toString();
            this.on(`${stateName}-show`, () => this.current = stateName);
        });

        this.transitions();
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

    transitions() {
        this.on('catalogs-next', () => {
            this.emit('catalogs-hide');
            this.emit('activities-show');
        });

        this.on('activities-next', () => {
            const activity = Storage.getDecoded('activity');

            switch(activity ? activity.value : null) {
                case 'search-books':
                    this.emit('search-books-request');
                    break;
                case 'latest-books':
                    this.emit('latest-books-request');
                    break;
                default:
                    console.error("Activity not defined.");
                    break;
            }
        });

        this.on('activities-step-back', () => {
            this.emit('activities-hide');
            this.emit('catalogs-show');
        });

        this.on('search-books-request', () => {
            this.emit('activities-hide');
            this.emit('search-profile-show');
        });

        this.on('latest-books-request', () => {
            const catalog = Storage.getDecoded('catalog');

            switch(catalog ? catalog.value : null) {
                case "4949":
                    this.emit('activities-hide');
                    this.emit('in-progress-show', 'activities');
                    break;
                case "5004":
                    this.emit('activities-hide');
                    this.emit('search-profile-show');
                    break;
                default:
                    console.error("No catalog defined.");
                    break;
            }
        });

        this.on('search-profile-step-back', () => {
            this.emit('search-profile-hide');
            this.emit(`activities-show`);
        });

        this.on('search-profile-results', () => {
            this.emit('search-profile-hide');
            if (Storage.getDecoded('profiles') !== null) {
                this.emit('confirm-profile-show');
            } else {
                this.emit('no-profile-show');
            }
        });

        this.on('confirm-profile-step-back', () => {
            this.emit('confirm-profile-hide');
            this.emit('search-profile-show');
        });

        this.on('confirm-profile-next', (profile) => {
            const activity = Storage.getDecoded('activity');

            switch(activity ? activity.value : null) {
                case 'search-books':
                    this.emit('shelves-request', profile)
                    break;
                case 'latest-books':
                    this.emit('confirm-profile-hide');
                    this.emit('in-progress-show', 'confirm-profile');
                    break;
                default:
                    console.error("No activity defined.");
                    break;
            }
        });

        this.on('no-profile-step-back', () => {
            this.emit('no-profile-hide');
            this.emit('search-profile-show');
        });

        this.on('shelves-results', () => {
            this.emit('confirm-profile-hide');
            this.emit('shelves-show');
        });

        this.on('shelves-step-back', () => {
            this.emit('shelves-hide');
            this.emit('confirm-profile-show');
        });

        this.on('search-catalog-request', () => {
            this.emit('shelves-hide');
            this.emit('in-progress-show', 'shelves');
        });

        this.on('in-progress-step-back', (caller) => {
            this.emit('in-progress-hide');
            this.emit(`${caller}-show`);
        });
    }
}


Object.assign(State.prototype, EventEmitter);


export default State;
