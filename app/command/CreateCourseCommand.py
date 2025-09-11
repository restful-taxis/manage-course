from typing import Optional
from pydantic import BaseModel


class CreateCourseCommand(BaseModel):
    point_depart: str
    point_arrivee: str
    userConnected: Optional[dict] = None