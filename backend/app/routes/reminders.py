from flask import Blueprint, jsonify, request
from psycopg import errors as pg_errors

from app.db import get_db
from app.errors import NotFoundError
from app.schemas.reminders import Reminders, RemindCreateRequest, RemindResponse

reminders_bp = Blueprint("Schedules", __name__)

# 一覧表示
#  @reminders_bp.get("/reminders")
#  def list_reminder():
#      query = Reminders.model_validate(request.args.to_dict())


# リマインダー登録
@reminders_bp.post("/reminders")
def create_remind():
    payload = request.get_json(silent=True) or {}
    body = RemindCreateRequest.model_validate(payload)

    db = get_db()

    try:
        with db.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO reminders
                        (title, comment, remind_at, notify_email, created_at, updated_at)
                    VALUES
                        (%(title)s,%(comment)s,%(remind_at)s,%(notify_email)s,now(), now())
                    RETURNING id, title, comment, remind_at, notify_email, is_notified, created_at, updated_at 
                """,
                body.model_dump(),
            )
            row = cur.fetchone()
        db.commit()

    # NotFoundErrorは登録処理だとおかしい。。。ので変更
    except ValueError:
        db.rollback()

    response_body = RemindResponse.model_validate(row).model_dump(
        mode="json", by_alias=True
    )

    return jsonify(response_body), 200


# 削除
@reminders_bp.delete("/reminders/<int:id>")
def delete_remind(id):
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute(
                """
                    DELETE FROM reminders 
                    WHERE id = %(id)s 
                    RETURNING id
                """,
                {
                    "id": id,
                },
            )
            row = cur.fetchone()

            if id < 1:
                raise ValueError("invalid: id must be greater than 0")

            if row is None:
                raise NotFoundError("not found: remind not found")
            
        db.commit()

    except NotFoundError:
        db.rollback()
        raise


    return ("", 204)


# まだよく分かっていないのでひとまずどんな方法ができるのか考えてみる
# 1.設定時間になったら
#    現在時刻との比較　or　時間になったら動く、のような判断ってできるのかによって内容変わりそう
# 2.データとして格納されている情報をSELECT
#    IDかID以外の何かを基準にデータを取りに行くように指示して、取得、DBにクエリ送信
# 3.送信処理
# 　　必要なもの→Resend　APIでメール送信が可能　設定


# メール送信処理
# 定期実行処理
# 通知済み管理


# バリデーション
# ログイン機能
