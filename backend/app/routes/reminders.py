from flask import Blueprint, jsonify, request
from psycopg import errors as pg_errors

from app.db import get_db
from app.errors import NotFoundError, BadRequestError
from app.schemas.reminders import (
    Reminders,
    RemindCreateRequest,
    RemindPutRequest,
    RemindResponse,
)

reminders_bp = Blueprint("Schedules", __name__)

# 一覧表示
# @reminders_bp.get("/reminders")
# def list_reminder():
#      query = RemindPutRequest.model_validate(request.args.to_dict())


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


# 更新
@reminders_bp.put("/reminders/<id>")
def put_remind(id):

    payload = request.get_json(silent=True)
    body = RemindPutRequest.model_validate(payload)
    db = get_db()

    try:
        with db.cursor() as cur:
            cur.execute(
                """
                    UPDATE reminders
                    SET
                        title = %(title)s,
                        comment = %(comment)s,
                        remind_at = %(remind_at)s,
                        notify_email = %(notify_email)s,
                        updated_at = now()
                    WHERE id = %(id)s
                    RETURNING *
                """,
                {
                    **body.model_dump(),
                    "id": id,
                },
            )
            row = cur.fetchone()

            if row is None:
                raise NotFoundError("not found: Remind not found")
        db.commit()

    except NotFoundError:
        db.rollback()
        raise

    response_body = RemindResponse.model_validate(row).model_dump(
        mode="json", by_alias=True
    )

    return jsonify(response_body), 200


# 削除
@reminders_bp.delete("/reminders/<id>")
def delete_remind(id: str):
    # idの検証を行う
    try:
        remind_id = int(id)
    except ValueError:
        raise BadRequestError("invalid: id must be an integer")

    if remind_id < 1:
        raise BadRequestError("invalid: id must be greater than 0")

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
                    "id": remind_id,
                },
            )
            row = cur.fetchone()

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
