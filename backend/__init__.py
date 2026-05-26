from flask import Flask
from flask_cors import CORS

#ここにはアプリ起動に必要な関数モデルやブループリントを登録
from app.config import Settings


def create_app() -> Flask:
    app = Flask(__name__)

