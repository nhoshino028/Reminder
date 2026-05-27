from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError

#エラーの定義をする
class APIError(Exception):
    code: str = "API_ERROR"  #文字列
    message: str = "api error"  #メッセージ
    status_code = int = 500  #HTTPステータスコード

    #カスタムメッセージ付きで例外を初期化する
    #APIerrorの中で意図して意図してraiseする
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

#エラーをjson形式にしてHTTPレスポンスとして返す
def register_error_handlers(app:Flask) -> None:

        @app.errorhandler(ValidationError)
        def _on_validation_error(e: ValidationError):
            details = [
                 {
                      "field": ".".join(str(p) for p in err["loc"]),
                      "reason": err["msg"],
                 }
                 for err in e.errors()
            ]
            return jsonify({
                 "code": "VALIDATION_ERROR",
                 "message": "request validation failed",
                 "details": details,
            }), 400
    