from typing import Optional
from pydantic import BaseModel


class ConfirmCourseCommand(BaseModel):
    userConnected: Optional[dict] = None