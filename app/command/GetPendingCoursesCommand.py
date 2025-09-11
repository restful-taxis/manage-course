from typing import Optional
from pydantic import BaseModel


class GetPendingCoursesCommand(BaseModel):
    userConnected: Optional[dict] = None