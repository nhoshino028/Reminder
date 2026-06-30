from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator


# 型チェック
class Reminders(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    title: str
    comment: str | None = None
    remind_at: datetime
    # EmailStr
    # メールアドレスとして不正な形式は弾いてくれるが、ドメイン制限やビジネスルールの追加を行いたい場合はカスタムバリデーションを利用する必要がありそう
    notify_email: EmailStr
    is_notified: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


# 登録
class RemindCreateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(min_length=1, max_length=100)
    comment: str = Field(max_length=1000)
    remind_at: datetime
    notify_email: EmailStr

    # 現在時刻より未来であること
    @field_validator("remind_at")
    @classmethod
    def _validate_remind_check(
        cls, value
    ) -> "RemindCreateRequest":  # RemindCreateRequestのインスタンス生成
        if value < datetime.now(timezone.utc):  # 現在日時と入力された日時を比較
            raise ValueError("remind_at must be after now")
        return value


# 更新
class RemindPutRequest(BaseModel):
    model_config = ConfigDict(popular_by_name=True)
    title: str = Field(max_length=100)
    comment: str | None = Field(max_length=1000)
    remind_at: datetime
    notify_email: EmailStr = Field(max_length=254)

    # 空文字でないこと（trim後1文字以上）(title)
    @field_validator("title", mode="before")
    @classmethod
    def empty_check(cls, value):
        if value.strip() == "":
            raise ValueError("title must not be empty")
        return value

    # タイムゾーンが含まれていること（remind_at）
    @field_validator("remind_at")
    @classmethod
    def timezone_check(cls, value):
        if value.tzinfo is None:
            raise ValueError("remind_at must include a timezone")
        return value

    # 現在時刻より未来であること（remind_at）
    @field_validator("remind_at")
    @classmethod
    def _validate_remind_check(
        cls, value
    ) -> "RemindCreateRequest":  # RemindCreateRequestのインスタンス生成
        if value < datetime.now(timezone.utc):  # 現在日時と入力された日時を比較
            raise ValueError("remind_at must be after now")
        return value


# レスポンスモデル（登録、更新時に必要　DBからのレスポンスを変換）
class RemindResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)  #

    id: int
    title: str
    comment: str | None = None
    remind_at: datetime
    notify_email: EmailStr
    is_notified: bool
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
