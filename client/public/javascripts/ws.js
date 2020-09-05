export default class WS {
    constructor() {
        let host = 'localhost',
            port = '8888';

        this.socket = new WebSocket(`ws://${host}:${port}/`);
        this.handlers = {};

        this.socket.onmessage = (event) => this.handle(event);
    }

    on(operation, handler) {
        this.handlers[operation] = this.handlers[operation] || [];
        this.handlers[operation].push(handler);
    }

    handle(event) {
        let message = JSON.parse(event.data),
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
            payload: message,
        }));
    }
}
