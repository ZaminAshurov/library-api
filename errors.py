from flask import jsonify


class HttpError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def http_error(message, status_code):
    return HttpError(message, status_code)


def register_error_handler(app):
    @app.errorhandler(HttpError)
    def handle_http_error(err):
        return jsonify({"error": err.message}), err.status_code