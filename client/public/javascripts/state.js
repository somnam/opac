import Storage from './storage.js';
import {EventEmitter} from './mixin/event_emitter.js';


class State {
    available_steps = [
        'catalogs',
        'activities',
        'search-profile',
        'no-profile',
        'confirm-profile',
        'shelves',
        'in-progress',
    ];

    constructor() {
        this.step = Storage.get('step') || 'init';

        this.available_steps.forEach((step) => {
            this.on(`${step}-show`, () => this.step = step);
        });

    }

    get step() {
        return this._step;
    }

    set step(value) {
        this._step = value;
        Storage.set('step', value);
    }

    restore() {
        switch(this.step) {
            case 'init':
                this.emit('catalogs-request');
                break;
            default:
                this.emit(`${this.step}-show`);
                break;
        }
    }
}


Object.assign(State.prototype, EventEmitter);


export default State;
