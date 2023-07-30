"use strict";

import Storage from './storage.js';
import {EventEmitter} from '../mixin/event_emitter.js';


class State {
    constructor(current) {
        this.current = Storage.get('current') || current;
    }

    get current() {
        return this._current;
    }

    set current(value) {
        this._current = value;
        Storage.set('current', value);
    }

    restore() {
        this.emit(`${this.current}-init`);
    }
}


Object.assign(State.prototype, EventEmitter);


export default State;
