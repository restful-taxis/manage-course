from typing import Optional
from pydantic import BaseModel


class CancelCourseCommand(BaseModel):
    userConnected: Optional[dict] = None