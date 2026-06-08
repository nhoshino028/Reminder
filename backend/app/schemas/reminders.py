from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr

#型チェック
class Reminders(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    name: str 
    title: str
    comment: str | None = None
    remind_at: datetime = Field(alias="remindAt")
    #EmailStr
    #メールアドレスとして不正な形式は弾いてくれるが、ドメイン制限やビジネスルールの追加を行いたい場合はカスタムバリデーションを利用する必要がありそう
    notify_email: EmailStr
    is_notified: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

#登録チェック
#リマインド時間が現在時刻よりも前の場合にエラーを返すような処理を入れる

class RemindCreateRequest(BaseModel):
    model_config = ConfigDict(popular_by_name=True)

    id: int
    name: str 
    title: str
    comment: str | None = None
    remind_at: datetime = Field(alias="remindAt")
    notify_email: EmailStr
    is_notified: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    #リマインド時間が現在時刻よりも前の場合にエラーを返す
    @model_validator(mode="after")
    def _time_check(self) -> "RemindCreateRequest": #RemindCreateRequestのインスタンス生成
        if self.remind_at < datetime.now(UTC)
            raise ValueError("remindAt must be after now")
        return self


#編集
#入力チェックが必要
    

#レスポンスモデル（登録、更新時に必要　DBからのレスポンスを）
class RemindRespose(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True) #