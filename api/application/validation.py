from flask import make_response
from werkzeug.exceptions import HTTPException
import json
from flask import current_app as app


class BusinessValidationError(HTTPException):
    error_code = None

    def __init__(self, status_code, error_code, message):
        self.message = message
        self.code = int(status_code)
        self.error_code = error_code
        super().__init__(description=self.message)

    def get_response(self, environ=None):
        response = super().get_response(environ)
        response.status_code = self.code
        return response


class InputValidationError(HTTPException):
    
    def __init__(self, status_code, message):
        self.message = message
        self.code = int(status_code)
        super().__init__(description=self.message)

    def get_response(self, environ=None):
        response = super().get_response(environ)
        response.status_code = self.code
        return response

class AuthenticationError(Exception):
    def __init__(self, message):
        super().__init__(message)

class BadRequestError(Exception):
    def __init__(self, message):
        super().__init__(message)

class NotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)

@app.errorhandler(BusinessValidationError)
def handle_business_validation_error(e):
    return {"message": e.message }, e.code

@app.errorhandler(InputValidationError)
def handle_input_validation_error(e):
    return {"message": e.message }, e.code

@app.errorhandler(AuthenticationError)
def handle_authentication_error(e):
    return {'message': str(e)}, 401

@app.errorhandler(BadRequestError)
def handle_bad_request_error(e):
    return {'message': str(e)}, 400

@app.errorhandler(NotFoundError)
def handle_not_found_error(e):
    return {'message': str(e)}, 404


@app.errorhandler(404)
def not_found(e):
    return {'message': str(e)}, 404