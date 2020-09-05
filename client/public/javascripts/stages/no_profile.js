import {FieldMixin} from '../mixin/field.js';
import {EventEmitter} from '../mixin/event_emitter.js';


class NoProfile {
    constructor() {
        this.on('no-profile-show', () => this.show('#no-profile-fields'));

        this.on('no-profile-hide', () => this.hide('#no-profile-fields'));

        this.on('search-profile-results', () => {
            if (this.storage.getItem('profileResults') === null)
                this.emit('no-profile-show');
        });
    }

    onDomLoaded() {
        const backBtn = document.querySelector('#no-profile-fields > #go-back-btn');
        backBtn.addEventListener('click', (event) => this.backBtnListener(event));
    }

    backBtnListener(event) {
        event.preventDefault();

        this.emit('no-profile-hide');
        this.emit('search-profile-show');
    }
}


Object.assign(NoProfile.prototype, EventEmitter);
Object.assign(NoProfile.prototype, FieldMixin);


export default NoProfile;
