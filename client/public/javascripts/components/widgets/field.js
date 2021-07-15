import {EventEmitter} from '../../mixin/event_emitter.js';


class Field {
    storage = localStorage;
    parser = new DOMParser();
    template = null;

    constructor(parentSelector) {
        this.parent = document.querySelector(parentSelector || '#app-form');
    }

    render() {
        return new Promise((resolve, reject) => {
            if (!this.template)
                reject(new Error("Field template not defined."));

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
