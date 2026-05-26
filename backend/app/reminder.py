from flask import blueprint
from psycopg import errors as pg_errors

from app.db import get_db
from app.errors import ConflictError, NotfoundError
from app.schemas.Reminders import Reminders

reminders_bp = Blueprint("Schedules", __name__)

@reminders_bp.get("/reminders")
def list_reminder():
    query = Reminders.model_validate(request.args.to_dict())

    