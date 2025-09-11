from sqlalchemy import Column, String, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.service.Database import Base
import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Enum

# Enum pour le statut de la course
class CourseStatus(PyEnum):
    DEMANDEE = "Demandée"
    VALIDEE = "Validée"
    EN_COURS = "En cours"
    TERMINEE = "Terminée"
    ANNULEE = "Annulée"

class Course(Base):
    __tablename__ = "course"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    chauffeur_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=True)
    point_depart = Column(String, nullable=False)
    point_arrivee = Column(String, nullable=False)
    date_heure_depart = Column(DateTime(timezone=True), nullable=True)
    date_heure_arrivee = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(CourseStatus), nullable=False, default=CourseStatus.DEMANDEE)
    tarif = Column(Numeric(10, 2), nullable=True)
    updatedAt = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)