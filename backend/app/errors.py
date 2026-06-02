from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError

#エラーの定義（処理時にはエラーの判別）をする
class APIError(Exception):
    code: str = "API_ERROR"  #文字列
    message: str = "api error"  #メッセージ
    status_code = int = 500  #HTTPステータスコード

    #カスタムメッセージ付きで例外を初期化する
    #APIerrorの中で意図してraiseする
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.message)
        if message is not None:
            self.message = message

#リソースが見つからない場合の例外
class NotFoundError(APIError):
    code = "NOT_FOUND"
    status_code: 404
    message = "resauce not found"

#一意制約や外部キー制約違反の例外
class ConflictError(APIError):
    code = "CONFLICT"
    status_code = 409
    message = "conflict"

#捕捉したエラーをjson形式にしてHTTPレスポンスとして返す処理
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
    
        @app.errorhandler(APIError)
        def _on_api_error(e: APIError):
             return jsonify({
                  "code": e.code,
                  "message": e.message,
                  "details": None,
             }), e.status_code
        
        @app.errorhandler(HTTPException)
        def _on_http_exception(e: HTTPException):
             return jsonify({
                  "code": "HTTP_ERROR",
                  "message": e.description,
                  "details": None,
             }), (e.code or 500)
        
        # 上記3つに該当しない例外を変換(3つ以外のものを捕捉してくれる)
        # stacktraceはapp.loger.exception()で出力し、外部にはサニタイズしたメッセージのみ返す
        # →開発者には詳細なエラーを表示し、外部には安全な内容だけを返すようになっている
        @app.errorhandler(Exception)
        def _on_unexpected(e: Exception):
             app.logger.exception("Unexpected error: %s", e)
             return jsonify({
                  "code": "INTERNAL_ERROR",
                  "message": "internal server error",
                  "details": None,
             }), 500