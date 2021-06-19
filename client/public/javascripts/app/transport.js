export default class Transport {
    constructor() {
        const host = 'localhost',
              port = '8888';

        return new Promise((resolve, reject) => {
            this.socket = new WebSocket(`ws://${host}:${port}/`);

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
}
