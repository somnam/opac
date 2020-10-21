import Storage from './storage.js';
import {EventEmitter} from '../mixin/event_emitter.js';
import Catalogs from '../stages/catalogs.js';
import Activities from '../stages/activities.js';
import SearchProfile from '../stages/search_profile.js';
import NoProfile from '../stages/no_profile.js';
import ConfirmProfile from '../stages/confirm_profile.js';
import Shelves from '../stages/shelves.js';
import InProgress from '../stages/in_progress.js';


class Stages {
    constructor() {
        this.catalogs = new Catalogs();
        this.activities = new Activities();
        this.searchProfile = new SearchProfile();
        this.noProfile = new NoProfile();
        this.confirmProfile = new ConfirmProfile();
        this.shelves = new Shelves();
        this.in_progress = new InProgress();

        this.setTransitions();
    }

    setTransitions() {
        this.on('catalogs-results', () => this.emit('catalogs-show'));

        this.on('activities-results', () => {
            this.emit('catalogs-hide');
            this.emit('activities-show');
        });

        this.on('activities-step-back', () => {
            this.emit('activities-hide');
            this.emit('catalogs-show');
        });

        this.on('search-books-request', () => {
            this.emit('activities-hide');
            this.emit('search-profile-show');
        });

        this.on('search-profile-step-back', (caller) => {
            this.emit('search-profile-hide');
            this.emit(`${caller}-show`);
        });

        this.on('latest-books-request', () => {
            this.emit('activities-hide');
            this.emit('in-progress-show', 'activities');
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


Object.assign(Stages.prototype, EventEmitter);


export default Stages;
