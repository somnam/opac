export let FieldMixin = {
    storage: localStorage,

    show(selector) {
        let fields = document.querySelector(selector);
        if (!fields)
            return

        fields.classList.add('fields');
        fields.classList.remove('fields-hidden');
    },

    hide(selector) {
        let fields = document.querySelector(selector);
        if (!fields)
            return;

        fields.classList.add('fields-hidden');
        fields.classList.remove('fields');
    },

    showLoading(btnSelector) {
        let btn = document.querySelector(btnSelector);
        btn.setAttribute('hidden', 'hidden');

        let loading = document.createElement('button');
        loading.setAttribute('id', 'loading-btn');
        loading.setAttribute('class', 'nes-btn is-disabled btn-block mb-4');
        loading.addEventListener('click', (event) => event.preventDefault());

        btn.after(loading);
    },

    hideLoading(btnSelector) {
        let btn = document.querySelector(btnSelector);
        btn.removeAttribute('hidden');

        let loading = btn.parentNode.querySelector('#loading-btn');
        if (loading !== null) {
            loading.remove();
        }
    },
};
