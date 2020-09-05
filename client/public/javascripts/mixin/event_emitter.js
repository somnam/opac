export let EventEmitter = {
    events: {},

    on(event, listener) {
        if (!this.events[event])
            this.events[event] = [];

        this.events[event].push(listener);
    },

    off(event, listener) {
        if (!this.events[event])
            return;

        const index = this.events[event].indexOf(listener);
        if (index === -1)
            return;

        this.events[event].splice(index, 1);
    },

    emit(event, ...args) {
        if (typeof this.events[event] !== 'object') {
            console.error(`Event ${event} not defined.`);
            return;
        }

        this.events[event].forEach((listener) => listener.apply(this, args));
    },

    once(event, listener) {
        this.on(event, (...args) => {
            this.off(event, listener);
            listener.apply(this, args);
        });
    },
};
