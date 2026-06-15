#モジュールの呼び出しを行う
from flask import Flask
from flask_cors import CORS

#ここにはアプリ起動に必要な関数モデルやブループリントを登録
from .config import Settings
from .db import init_app as init_db
from .errors import register_error_handlers
from app.routes.health import health_bp
from app.routes.reminders import reminders_bp

def create_app() -> Flask:
    app = Flask(__name__)
    
    #register_error_handlers(app)を登録
    register_error_handlers(app)

    settings = Settings()
    app.config["SETTINGS"] = settings #接続情報を保存
    app.json.sort_keys = False
    app.json.ensure_ascii = False
    app.debug = settings.flask_debug

    init_db(app)

    #クロスオリジンリソース共有→異なるオリジン（ここでいう"http://localhost:5173","http://localhost:8080"）との通信を許可する
    #許可したドメインのみのアクセスにすることでセキュリティ性を損なわない
    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173",
                    "http://localhost:8080",
                ]
            }
        },
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_header=["Content-Type"],
    )

    app.register_blueprint(health_bp)
    app.register_blueprint(reminders_bp)

    return app