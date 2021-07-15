export default class Loading {
    constructor(...selectors) {
        this.selectors = selectors;
    }

    show() {
        let loading = document.createElement('div')
        loading.setAttribute('class', 'nes-text is-primary text-center loading-text');

        this.selectors
            .map((selector) => document.querySelector(selector))
            .filter((selector) => !!selector)
            .forEach((container) => container.appendChild(loading));
    }

    hide() {
        let loading = document.querySelector('.loading-text');

        if (loading !== null) {
            loading.remove();
        }
    }
}
