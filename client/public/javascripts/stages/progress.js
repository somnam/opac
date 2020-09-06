import {FieldMixin} from '../mixin/field.js';
import {EventEmitter} from '../mixin/event_emitter.js';


class Progress {
    constructor() {
        this.step = this.storage.getItem('step') || 'search-profile';

        this.on('search-profile-show', () => {
            this.step = 'search-profile';
            this.setProgress();
        });

        this.on('confirm-profile-show', () => {
            this.step = 'confirm-profile';
            this.setProgress();
        });

        this.on('no-profile-show', () => {
            this.step = 'no-profile';
            this.setProgress();
        });

        this.on('shelves-show', () => {
            this.step = 'shelves';
            this.setProgress();
        });

        this.on('catalogs-show', () => {
            this.step = 'catalogs';
            this.setProgress();
        });
    }

    get step() {
        return this._step;
    }

    set step(value) {
        this._step = value;
        this.storage.setItem('step', value);
    }

    onDomLoaded() {
        this.setProgress();
        this.showStep();
    }

    setProgress() {
        document.querySelectorAll('#progress > .nes-progress').forEach(
            (progress) => progress.value = 0
        );

        switch(this.step) {
            case 'catalogs':
                document.querySelector('#catalogs-step').value = 1;
            case 'shelves':
                document.querySelector('#shelves-step').value = 1;
            case 'confirm-profile':
                document.querySelector('#confirm-profile-step').value = 1;
            case 'no-profile':
            case 'search-profile':
                document.querySelector('#search-profile-step').value = 1;
                break;
        }
    }

    showStep() {
        switch(this.step) {
            case 'search-profile':
                this.emit('search-profile-show');
                break;
            case 'no-profile':
                this.emit('no-profile-show');
                break;
            case 'confirm-profile':
                this.emit('confirm-profile-show');
                break;
            case 'shelves':
                this.emit('shelves-show'); 
                break;
            case 'catalogs':
                this.emit('catalogs-show');
                break;
        }
    }
}


Object.assign(Progress.prototype, EventEmitter);
Object.assign(Progress.prototype, FieldMixin);


export default Progress;
