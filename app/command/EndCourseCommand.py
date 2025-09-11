from typing import Optional
from pydantic import BaseModel


class EndCourseCommand(BaseModel):
    userConnected: Optional[dict] = None