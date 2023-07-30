"use strict";

import { EventEmitter } from '../mixin/event_emitter.js';
import { NotImplementedError } from '../app/exception.js';


class Field {
    storage = localStorage;
    parser = new DOMParser();
    template = null;

    constructor(transport, parentSelector = '#app-form') {
        this.transport = transport;

        this.parent = document.querySelector(parentSelector);

        this.on(`${this}-init`, (message) => this.onInit(message));

        this.on(`${this}-show`, () => this.onShow());

        this.on(`${this}-hide`, () => this.onHide());

        this.on(`${this}-next`, () => this.onNext());

        this.on(`${this}-back`, () => this.onBack());
    }

    static toString() { throw new NotImplementedError() }

    toString() { return this.__proto__.constructor.toString() }

    onInit(message = null) { this.emit(`${this}-show`); }

    onShow() {
        this.render()
            .then(() => this.onRender())
            .catch(error => console.error(error));
    }

    onRender() { }

    onHide() { this.remove() }

    onNext() { }

    onBack() { }

    render() {
        return new Promise((resolve, reject) => {
            if (!this.template) {
                reject(new NotImplementedError());
            }

            this.remove();

            this.parent.insertAdjacentHTML('afterbegin', this.template.trim());

            resolve();
        });
    }

    remove() {
        this.parent.childNodes.forEach((node) => node.remove());
    }
}


Object.assign(Field.prototype, EventEmitter);


export default Field;
