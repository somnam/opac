import {EventEmitter} from '../mixin/event_emitter.js';


export default class Pager {
    constructor(parentId, onClickEvent) {
        this.parentId = parentId;
        this.onClickEvent = onClickEvent;
        this.prevBtn = null;
        this.nextBtn = null;
    }

    makePageBtn(type, page) {
        let btn = document.createElement('button');

        btn.setAttribute('type', 'button');
        btn.setAttribute('class', `nes-btn is-success btn-${type}`);
        btn.setAttribute('data-page', page);
        btn.appendChild(document.createElement('span'))

        btn.addEventListener('click', (event) => {
            event.preventDefault();

            if (this.onClickEvent !== null) {
                this.emit(this.onClickEvent, parseInt(event.target.dataset.page));
            }
        });

        document.querySelector(`#${this.parentId}`).appendChild(btn);

        return btn;
    }

    hidePageBtn(btn) {
        if (btn !== null) {
            btn.remove();
        }
    }

    update(prevPage, nextPage) {
        if (!document.querySelector(`#${this.parentId}`))
            throw new Error(`Parent element #${this.parentId} not found.`);

        this.hidePageBtn(this.prevBtn);
        this.hidePageBtn(this.nextBtn);

        if (prevPage) {
            this.prevBtn = this.makePageBtn('prevPage', prevPage);
        }

        if (nextPage) {
            this.nextBtn = this.makePageBtn('nextPage', nextPage);
        }
    }
}

Object.assign(Pager.prototype, EventEmitter);
