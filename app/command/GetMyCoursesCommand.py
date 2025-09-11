from typing import Optional
from pydantic import BaseModel


class GetMyCoursesCommand(BaseModel):
    userConnected: Optional[dict] = None