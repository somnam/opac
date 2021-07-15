export default class LoadingBtn {
    constructor(selector) {
        this.selector = selector;
    }

    show() {
        let btn = document.querySelector(this.selector);
        btn.setAttribute('hidden', 'hidden');

        let loading = document.createElement('button');
        loading.setAttribute('id', 'loading-btn');
        loading.setAttribute('class', 'nes-btn is-disabled btn-block mb-4');
        loading.addEventListener('click', (event) => event.preventDefault());

        btn.after(loading);
    }

    hide() {
        let btn = document.querySelector(this.selector);
        btn.removeAttribute('hidden');

        let loading = btn.parentNode.querySelector('#loading-btn');
        if (loading !== null) {
            loading.remove();
        }
    }
}
