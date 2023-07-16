export default class Storage {
    static get(item) {
        return localStorage.getItem(item);
    }

    static set(item, value) {
        localStorage.setItem(item, value);
    }

    static remove(...items) {
        for (const item of items) {
            localStorage.removeItem(item);
        }
    }

    static removeAll() {
        localStorage.clear();
    }

    static getDecoded(item) {
        return JSON.parse(localStorage.getItem(item));
    }

    static setEncoded(item, value) {
        localStorage.setItem(item, JSON.stringify(value));
    }
}
