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

export class ProfileNotFoundError extends Error {
    constructor(message) {
        super(message || "");
        this.name = "ProfileNotFoundError";
        this.code = 404;
    }
}
