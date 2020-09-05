import Adapter from './adapter.js';
import Progress from './stages/progress.js';
import SearchProfile from './stages/search_profile.js';
import NoProfile from './stages/no_profile.js';
import ConfirmProfile from './stages/confirm_profile.js';
import Shelves from './stages/shelves.js';
import Libraries from './stages/libraries.js';


class WebSocketApp {
    constructor() {
        this.adapter = new Adapter();
        this.progress = new Progress();
        this.searchProfile = new SearchProfile();
        this.noProfile = new NoProfile();
        this.confirmProfile = new ConfirmProfile();
        this.shelves = new Shelves();
        this.libraries = new Libraries();
    }

    onDomLoaded() {
        this.progress.onDomLoaded();
        this.searchProfile.onDomLoaded();
        this.noProfile.onDomLoaded();
        this.confirmProfile.onDomLoaded();
        this.shelves.onDomLoaded();
        this.libraries.onDomLoaded();
    }
}


document.addEventListener("DOMContentLoaded", function() {
    (new WebSocketApp()).onDomLoaded();
})
