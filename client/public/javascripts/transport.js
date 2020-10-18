export default class Transport {
    constructor() {
        const host = 'localhost',
              port = '8888';

        return new Promise((resolve, reject) => {
            this.socket = new WebSocket(`ws://${host}:${port}/`);
            this.handlers = {};

            this.socket.onmessage = (event) => this.handle(event);

            this.socket.onopen = (event) => resolve(this);
            this.socket.onerror = (error) => reject(error);
        });
    }

    on(operation, handler) {
        this.handlers[operation] = this.handlers[operation] || [];
        this.handlers[operation].push(handler);
    }

    handle(event) {
        const message = JSON.parse(event.data),
              operation = message.operation;

        if (this.handlers.hasOwnProperty(operation)) {
            this.handlers[operation].forEach(handler => handler(message))
        } else {
            console.error(`Handler for operation ${operation} not defined.`)
        }
    }

    send(operation, message) {
        this.socket.send(JSON.stringify({
            operation: operation,
            payload: message || null,
        }));
    }
}
