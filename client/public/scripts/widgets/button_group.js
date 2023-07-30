"use strict";

import Storage from '../app/storage.js';


export default class ButtonGroup {
    constructor(collectionName, optionClass, containerId) {
        this.containerId = containerId || `${collectionName}-group`;
        this.optionClass = optionClass || "";
        this.options = [];
    }

    makeOptions() {
        let options = new DocumentFragment();

        this.options.forEach(option => {
            let element = document.createElement('button');
            element.setAttribute('class', `nes-btn ${this.optionClass}`);
            element.setAttribute('type', 'button');
            element.innerHTML = option.name;

            options.append(element);
        });

        return options;
    }

    makeContainer() {
        const currentContainer = document.querySelector(`#${this.containerId}`);

        let container = document.createElement('div');
        container.setAttribute('class', currentContainer.className);
        container.setAttribute('id', this.containerId);
        return container;
    }

    update(options) {
        if (!!options) {
            this.options = options;
        }

        const container = this.makeContainer();
        container.appendChild(this.makeOptions());

        const currentContainer = document.querySelector(`#${this.containerId}`);
        currentContainer.replaceWith(container);
    }

}
