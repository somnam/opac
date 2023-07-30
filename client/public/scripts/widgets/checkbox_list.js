"use strict";

import Storage from '../app/storage.js';


class CheckboxListState {
    constructor(collectionName, optionName, filter) {
        this.collectionName = collectionName;
        this.optionName = optionName;
        this.filter = filter;
    }

    get options() {
        const options = Storage.getDecoded(this.collectionName);

        let items = options ? options.items : [];

        if (items.length && this.filter !== undefined) {
            items = this.filter(items);
        }

        return items
    }

    get checked() {
        const checked = Storage.getDecoded(this.optionName);
        return checked ? checked : [];
    }
}

export default class CheckboxList {
    constructor(collectionName, optionName, filter) {
        this.id = `${optionName}-list`;
        this.name = optionName;
        this.state = new CheckboxListState(collectionName, optionName, filter);
        this.checked = [];
    }

    makeOptions() {
        let options = new DocumentFragment();

        this.checked = this.state.checked;

        this.state.options.forEach(option => {
            let input = document.createElement('input');
            input.setAttribute('class', 'nes-checkbox');
            input.setAttribute('type', 'checkbox');
            input.setAttribute('name', this.name);
            input.setAttribute('value', option.value)

            if (this.checked.some(elem => elem.value === option.value)) {
                input.setAttribute('checked', '');
            }

            let span = document.createElement('span');
            span.innerHTML = option.name;

            let label = document.createElement('label');
            label.appendChild(input);
            label.appendChild(span);

            input.addEventListener('click', (event) => this.toggleChecked(event));

            options.append(label);
        });

        return options;
    }

    toggleChecked(event) {
        const value = event.target.value;

        if (this.checked.some(elem => elem.value === value)) {
            this.checked = this.checked.filter(elem => elem.value !== value);
        } else {
            const option = this.state.options.find(opt => opt.value === value);
            this.checked.push(option);
        }

        Storage.setEncoded(this.name, this.checked);
    }

    makeContainer() {
        let container = document.createElement('div');
        container.setAttribute('class', 'item');
        container.setAttribute('id', this.id);
        return container;
    }

    update() {
        const container = this.makeContainer();
        container.appendChild(this.makeOptions());

        const currentContainer = document.querySelector(`#${this.id}`);
        currentContainer.replaceWith(container);
    }
}
