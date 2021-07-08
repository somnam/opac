import Storage from '../../app/storage.js';


class RadioListState {
    constructor(collectionName, optionName) {
        this.collectionName = collectionName;
        this.optionName = optionName;
    }

    get options() {
        const options = Storage.getDecoded(this.collectionName);
        return options ? options.items : [];
    }

    get checked() {
        const checked = Storage.getDecoded(this.optionName);
        return checked ? checked : this.options.length ? this.options[0] : null;
    }
}

export default class RadioList {
    constructor(collectionName, optionName) {
        this.id = `${optionName}-list`;
        this.name = optionName;
        this.state = new RadioListState(collectionName, optionName);
    }

    makeOptions() {
        let options = new DocumentFragment();

        const checked = this.state.checked;

        this.state.options.forEach(option => {
            let input = document.createElement('input');
            input.setAttribute('class', 'nes-radio');
            input.setAttribute('type', 'radio');
            input.setAttribute('name', this.name);
            input.setAttribute('value', option.value)

            if (checked && option.value === checked.value) {
                input.setAttribute('checked', '');
            }

            let span = document.createElement('span');
            span.innerHTML = option.name;

            let label = document.createElement('label');
            label.appendChild(input);
            label.appendChild(span);

            options.append(label);
        });

        return options;
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

    get checked() {
        const checked = document.querySelector(`input[name="${this.name}"]:checked`);
        if (!checked)
            return null;

        const checkedIdx = this.state.options.findIndex(opt => {
            return opt.value === checked.value;
        });

        return checkedIdx !== -1 ? this.state.options[checkedIdx] : null;
    }
}
