export class NotImplementedError extends Error {
    constructor(message) {
        super(message || "");
        this.name = "NotImplementedError";
    }
}

export class TemplateNotDefinedError extends Error {
    constructor(message) {
        super(message || "");
        this.name = "NotDefinedError";
    }
}