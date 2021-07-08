import {EventEmitter} from '../../mixin/event_emitter.js';


class Field {
    storage = localStorage;
    parser = new DOMParser();
    template = null;

    constructor(parentSelector) {
        this.parentSelector = parentSelector || '#app-form';
        this.dom = null;
        this.node = null;
    }

    render() {
        return new Promise((resolve, reject) => {
            if (!this.template)
                reject(new Error("Field template not defined."));

            this.remove();

            if (!this.dom) {
                const parsed = this.parser.parseFromString(this.template, 'text/html');
                this.dom = parsed.querySelector('template');
            }

            this.node = document.createElement('div');
            this.node.append(this.dom.content.cloneNode(true));

            document.querySelector(this.parentSelector).append(this.node);

            resolve(this.node);
        });
    }

    remove() {
        if (!this.node)
            return
        this.node.remove();
    }

    showLoading(btnSelector) {
        let btn = document.querySelector(btnSelector);
        btn.setAttribute('hidden', 'hidden');

        let loading = document.createElement('button');
        loading.setAttribute('id', 'loading-btn');
        loading.setAttribute('class', 'nes-btn is-disabled btn-block mb-4');
        loading.addEventListener('click', (event) => event.preventDefault());

        btn.after(loading);
    }

    hideLoading(btnSelector) {
        let btn = document.querySelector(btnSelector);
        btn.removeAttribute('hidden');

        let loading = btn.parentNode.querySelector('#loading-btn');
        if (loading !== null) {
            loading.remove();
        }
    }
}


Object.assign(Field.prototype, EventEmitter);


export default Field;
