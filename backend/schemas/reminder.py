from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class Reminders(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    name: str 
    title: str
    comment: str | None = None
    remind_at: datetime = Field(alias="remindAt")
    notify_email: EmailStr
    is_notified: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
