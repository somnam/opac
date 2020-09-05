import {EventEmitter} from '../mixin/event_emitter.js';


export class PagerParams {
    constructor(prevPage, nextPage) {
        this.prevPage = prevPage;
        this.nextPage = nextPage;
    }
}


export class Pager {
    constructor(parentId, onClickEvent) {
        this.parent = document.querySelector(`#${parentId}`);
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

        this.parent.appendChild(btn);

        return btn;
    }

    hidePageBtn(btn) {
        if (btn !== null) {
            btn.remove();
        }
    }

    update(pagerParams) {
        this.hidePageBtn(this.prevBtn);
        this.hidePageBtn(this.nextBtn);

        if (pagerParams.prevPage) {
            this.prevBtn = this.makePageBtn('prevPage', pagerParams.prevPage);
        }

        if (pagerParams.nextPage) {
            this.nextBtn = this.makePageBtn('nextPage', pagerParams.nextPage);
        }
    }
}

Object.assign(Pager.prototype, EventEmitter);
