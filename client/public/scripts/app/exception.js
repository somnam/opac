"use strict";

export class NotImplementedError extends Error {
    constructor(message) {
        super(message || "");
        this.name = "NotImplementedError";
        this.code = 500;
    }
}

export class InternalServerError extends Error {
    constructor(message) {
        super(message || "");
        this.name = "InternalServerError";
        this.code = 500;
    }
}

export class NotFoundError extends Error {
    constructor(message) {
        super(message || "");
        this.name = "NotFoundError";
        this.code = 404;
    }
}
