from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class Reminders(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    name: str 
    title:
    comment:
    remind_at:
    notify_email:
    is_notified:
    created_at:
    updated_at:
