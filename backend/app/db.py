import psycopg from psycopg import dict_row
from flask import Flask, g, current_app  #gオブジェクトは１回のリクエスト間で有効な情報を保持してくれるグローバルオブジェクト

#現在のFlaskリクエストに基づくpsycopgの接続を返す
def get_db() -> psycopg.Connection:  #リクエストごとにデータべース接続を取得する
    if "db" not in g:
        settings = current_app.config["SETTINGS"]
        g.db = psycopg.connect(
            settings.database_url,
            row_factory=dict_row,
            autocommit=False,
        )
    return g.db

#接続を閉じる
def close_db(exc: BaseException | None = None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()

#close_dbを登録する
#登録するとリクエスト終了時にclose_dbが呼ばれて確実に接続が閉じる
def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)