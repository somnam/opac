import {EventEmitter} from './mixin/event_emitter.js';


class State {
    storage = localStorage;
    steps = [
        'catalogs',
        'activities',
        'search-profile',
        'no-profile',
        'confirm-profile',
        'shelves',
        'in-progress',
    ];

    constructor() {
        this.step = this.storage.getItem('step') || 'init';

        this.steps.forEach((step) => {
            this.on(`${step}-show`, () => this.step = step);
        });
    }

    get step() {
        return this._step;
    }

    set step(value) {
        this._step = value;
        this.storage.setItem('step', value);
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
