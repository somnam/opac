export class RadioListParams {
    constructor(items, checked) {
        this.items = items;
        this.checked = checked;
    }

    checkedIdx() {
        if (this.checked == null)
            return 0;

        const checkedIdx = this.items.findIndex(
            (elem) => elem.value === this.checked.value
        );
        return (checkedIdx !== -1) ? checkedIdx: 0;
    }
}

export class RadioList {
    constructor(parentId, name) {
        this.parent = document.querySelector(`#${parentId}`);
        this.id = `${name}-list`;
        this.name = name;
    }

    makeItemsList(radioListParams) {
        let itemsList = new DocumentFragment();

        const items = radioListParams.items,
              checkedIdx = radioListParams.checkedIdx();

        items.forEach((item, idx) => {
            let input = document.createElement('input');
            input.setAttribute('class', 'nes-radio');
            input.setAttribute('type', 'radio');
            input.setAttribute('name', this.name);
            input.setAttribute('value', item.value)

            if (idx === checkedIdx) {
                input.setAttribute('checked', '');
            }

            let span = document.createElement('span');
            span.innerHTML = item.name;

            let label = document.createElement('label');
            label.appendChild(input);
            label.appendChild(span);

            itemsList.append(label);
        });

        return itemsList;
    }

    makeListContainer(radioListParams) {
        const itemsList = this.makeItemsList(radioListParams);

        let newShelvesContainer = document.createElement('div');

        newShelvesContainer.setAttribute('class', 'item');
        newShelvesContainer.setAttribute('id', this.id);

        newShelvesContainer.appendChild(itemsList);

        return newShelvesContainer;
    }

    update(radioListParams) {
        const listContainer = this.makeListContainer(radioListParams);

        const currentListContainer = document.querySelector(`#${this.id}`);
        currentListContainer.replaceWith(listContainer);
    }
}
