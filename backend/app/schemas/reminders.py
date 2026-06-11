from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator

#型チェック
class Reminders(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    title: str
    comment: str | None = None
    remind_at: datetime = Field(alias="remindAt")
    #EmailStr
    #メールアドレスとして不正な形式は弾いてくれるが、ドメイン制限やビジネスルールの追加を行いたい場合はカスタムバリデーションを利用する必要がありそう
    notify_email: EmailStr
    is_notified: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


#登録
class RemindCreateRequest(BaseModel):
    model_config = ConfigDict(popular_by_name=True)

    title: str
    comment: str | None = None
    remind_at: datetime = Field(alias="remindAt")
    notify_email: EmailStr

    #リマインド時間が現在時刻よりも前の場合にエラーを返す
    @field_validator("remind_at")
    @classmethod
    def _validate_remind_check(cls, value) -> "RemindCreateRequest": #RemindCreateRequestのインスタンス生成
        if value < datetime.now(timezone.utc): #現在日時と入力された日時を比較
            raise ValueError("remindAt must be after now")
        return value
    



#編集
#入力チェックが必要
    

#レスポンスモデル（登録、更新時に必要　DBからのレスポンスを変換）
class RemindResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True) #

    id: int
    title: str
    comment: str | None = None
    remind_at: datetime = Field(alias="remindAt")
    notify_email: EmailStr
    is_notified: bool
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")