"use strict";

export default class DataTable {
    constructor(name, headers) {
        this.id = `${name}-table`;
        this.name = name;
        this.headers = headers;
    }

    makeContainer() {
        const container = document.createElement('div');
        container.setAttribute('class', 'nes-table-responsive');
        container.setAttribute('id', this.id);

        return container;
    }

    makeTable(items) {
        const table = document.createElement('table');
        table.setAttribute('class', 'nes-table is-bordered is-centered');

        table.appendChild(this.makeHeader());

        if (items !== null && items !== undefined) {
            table.appendChild(this.makeBody(items));
        }

        return table;
    }

    makeHeader() {
        const head = document.createElement('thead');
        const tr = document.createElement('tr');

        this.headers.forEach((header) => {
            const th = document.createElement('th');
            th.innerHTML = header;
            tr.appendChild(th);
        });

        head.appendChild(tr);

        return head;
    }

    makeBody(items) {
        const body = document.createElement('tbody');

        items.forEach((item) => {
            const tr = document.createElement('tr');

            this.headers.forEach((header) => {
                const td = document.createElement('td');

                if (item.hasOwnProperty(header)) {
                    td.innerHTML = item[header];
                }

                tr.appendChild(td);
            });

            body.appendChild(tr);
        })

        return body;
    }

    update(items) {
        const container = this.makeContainer();

        container.appendChild(this.makeTable(items));

        const currentContainer = document.querySelector(`#${this.id}`);

        currentContainer.replaceWith(container);
    }
}
