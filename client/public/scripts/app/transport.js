"use strict";

import Storage from './storage.js';

export default class Transport {
    constructor(host, port, secure = true) {
        this.host = host;
        this.port = port;
        this.ws_schema = secure ? "wss" : "ws";
        this.http_schema = secure ? "https" : "http";

        return new Promise((resolve, reject) => {
            this.socket = new WebSocket(`${this.ws_schema}://${this.host}:${this.port}/ws`);
            this.socket.onopen = (event) => resolve(this);
            this.socket.onerror = (error) => reject(error);
        });
    }

    get(endpoint, params) {
        const url = new URL(`${this.http_schema}://${this.host}:${this.port}/${endpoint}`);

        if (params !== undefined && params !== null) {
            url.search = new URLSearchParams(params).toString();
        }

        return fetch(url, {
            method: "GET",
            headers: { 'Content-Type': 'application/json;charset=utf-8' },
        })
    }

    post(endpoint, message) {
        let body = null;
        if (message !== undefined && message !== null) {
            body = JSON.stringify(message);
        }

        const url = new URL(`${this.http_schema}://${this.host}:${this.port}/${endpoint}`);

        return fetch(url, {
            method: "POST",
            headers: { 'Content-Type': 'application/json;charset=utf-8' },
            body: body,
        })
    }

    request(operation, message) {
        this.socket.send(JSON.stringify({
            operation: operation,
            payload: message || null,
        }));

        return new Promise((resolve, reject) => {
            this.socket.onmessage = (event) => resolve(JSON.parse(event.data));
            this.socket.onerror = (error) => reject(error);
        })
    }
}
