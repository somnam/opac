import { EventEmitter } from '../../mixin/event_emitter.js';
import { NotImplementedError } from '../../app/exception.js';


class Field {
    storage = localStorage;
    parser = new DOMParser();
    template = null;

    constructor(parentSelector) {
        this.parent = document.querySelector(parentSelector || '#app-form');

        this.on(`${this}-request`, (message) => this.onRequest(message));

        this.on(`${this}-data`, () => this.onData());

        this.on(`${this}-show`, () => this.onShow());

        this.on(`${this}-hide`, () => this.onHide());

        this.on(`${this}-next`, () => this.onNext());

        this.on(`${this}-back`, () => this.onBack());
    }

    static toString() { throw new NotImplementedError() }

    toString() { return this.__proto__.constructor.toString() }

    onRequest(message = null) { this.emit(`${this}-data`, message); }

    onData() { this.emit(`${this}-show`) }

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
            if (!this.template)
                reject(new NotImplementedError());

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
