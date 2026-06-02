from pydantic_settings import BaseSettings, SettingsConfigDict

#環境設定やDBへの接続情報をまとめたクラス
class Settings(BaseSettings):
    database_url: str = ""
    flask_debug: bool = False

    #直接実行（python app.pyのように）するときに.envを読み込んで動作するよう設定（フォールバック）
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )