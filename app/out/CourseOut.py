from pydantic import BaseModel
import uuid
from datetime import datetime
from enum import Enum


class CourseStatus(str, Enum):
    DEMANDEE = "Demandée"
    VALIDEE = "Validée"
    EN_COURS = "En cours"
    TERMINEE = "Terminée"
    ANNULEE = "Annulée"


class CourseOut(BaseModel):
    id: uuid.UUID
    client_id: uuid.UUID
    chauffeur_id: uuid.UUID | None
    point_depart: str
    point_arrivee: str
    date_heure_depart: datetime | None
    date_heure_arrivee: datetime | None
    status: CourseStatus
    tarif: float | None
    updatedAt: datetime

    model_config = {
        "from_attributes": True
    }