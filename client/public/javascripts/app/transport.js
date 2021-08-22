import Handler from "./handler.js";

export default class Transport {
    constructor() {
        const host = 'localhost',
              port = '8888';

        return new Promise((resolve, reject) => {
            this.socket = new WebSocket(`ws://${host}:${port}/`);

            this.handler = new Handler(this);

            this.socket.onopen = (event) => resolve(this);

            this.socket.onerror = (error) => reject(error);
        });
    }

    onmessage(callback) {
        this.socket.onmessage = callback;
    }

    send(operation, message) {
        this.socket.send(JSON.stringify({
            operation: operation,
            payload: message || null,
        }));
    }

    fetch(operation, message) {
        return new Promise((resolve, reject) => {
            this.send(operation, message);

            this.onmessage((event) => this.handler.handle(event)
                .then(() => resolve())
                .catch(error => reject(error))
            );
        })
    }
}
