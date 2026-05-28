from flask import blueprint
from psycopg import errors as pg_errors

from app.db import get_db
from app.errors import ConflictError, NotfoundError
from app.schemas.Reminders import Reminders

reminders_bp = Blueprint("Schedules", __name__)

#一覧表示
#  @reminders_bp.get("/reminders")
#  def list_reminder():
#      query = Reminders.model_validate(request.args.to_dict())

#リマインダー登録
@reminders_bp.post("/reminders")
def create_remind():
    payload = request.get_json(silent=True) or {}
    body = 

#編集

#削除


#まだよく分かっていないのでひとまずどんな方法ができるのか考えてみる
# 1.設定時間になったら
#    現在時刻との比較　or　時間になったら動く、のような判断ってできるのかによって内容変わりそう
# 2.データとして格納されている情報をSELECT
#    IDかID以外の何かを基準にデータを取りに行くように指示して、取得、DBにクエリ送信
# 3.送信処理
#　　必要なもの→Resend　APIでメール送信が可能　設定


#メール送信処理
#定期実行処理
#通知済み管理


#バリデーション
#ログイン機能