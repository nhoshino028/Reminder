from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError

class APIError(Exception):
    code: str = "API_ERROR"
    message: str = "api_error"
    status_code = int = 500


    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.message)
        if message is not None:
            self.message = message

class NotFoundError(APIError):
    code = "NOT_FOUND"
    status_code: 404
    message = "resauce not found"

class ConflictError(APIError):
    code = "CONFLICT"
    status_code = 409
    message = "conflict"

class ValidationError(APIError)
    