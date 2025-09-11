from typing import Optional
from pydantic import BaseModel


class StartCourseCommand(BaseModel):
    userConnected: Optional[dict] = None