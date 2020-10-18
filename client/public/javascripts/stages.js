import Catalogs from './stages/catalogs.js';
import Activities from './stages/activities.js';
import SearchProfile from './stages/search_profile.js';
import NoProfile from './stages/no_profile.js';
import ConfirmProfile from './stages/confirm_profile.js';
import Shelves from './stages/shelves.js';
import InProgress from './stages/in_progress.js';


// FIXME: replace class with a better solution.
export default class Stages {
    constructor() {
        this.catalogs = new Catalogs();
        this.activities = new Activities();
        this.searchProfile = new SearchProfile();
        this.noProfile = new NoProfile();
        this.confirmProfile = new ConfirmProfile();
        this.shelves = new Shelves();
        this.in_progress = new InProgress();
    }
}
