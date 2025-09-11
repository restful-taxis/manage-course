from typing import Optional
from pydantic import BaseModel


class DeleteCourseCommand(BaseModel):
    userConnected: Optional[dict] = None