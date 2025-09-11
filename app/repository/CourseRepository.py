import uuid
from typing import Optional
from datetime import datetime, timezone

from app.command.CreateCourseCommand import CreateCourseCommand
from app.command.ConfirmCourseCommand import ConfirmCourseCommand
from app.models.Course import Course, CourseStatus
from app.service.Database import Database


class CourseRepository:
    @Database.with_session
    def createCourse(self, course_in: CreateCourseCommand, db=None) -> Course:

        # Vérifier que l'utilisateur est bien un customer
        user_roles = (course_in.userConnected or {}).get("roles", [])
        if "customer" not in user_roles:
            raise ValueError("Seuls les customers peuvent créer une course")

        entity = Course(
            client_id=uuid.UUID(course_in.userConnected["id"]),
            point_depart=course_in.point_depart,
            point_arrivee=course_in.point_arrivee,
            # Les autres champs prennent leurs valeurs par défaut
        )

        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    @Database.with_session
    def getCourseById(self, course_id: uuid.UUID, db=None) -> Optional[Course]:
        return db.query(Course).filter(Course.id == course_id).first()

    @Database.with_session
    def confirmCourse(self, course_id: uuid.UUID, user_connected: dict, db=None) -> Course:
        # Vérifier que l'utilisateur est bien un driver
        user_roles = (user_connected or {}).get("roles", [])
        if "driver" not in user_roles:
            raise ValueError("Seuls les drivers peuvent confirmer une course")

        # Récupérer la course
        course = self.getCourseById(course_id, db=db)
        if not course:
            raise ValueError("Course non trouvée")

        # Vérifier que la course est bien à l'état "demandée"
        if course.status != CourseStatus.DEMANDEE:
            raise ValueError("Seules les courses demandées peuvent être confirmées")

        # Mettre à jour la course
        course.status = CourseStatus.VALIDEE
        course.chauffeur_id = uuid.UUID(user_connected["id"])
        course.updatedAt = datetime.utcnow()

        db.commit()
        db.refresh(course)
        return course

    @Database.with_session
    def cancelCourse(self, course_id: uuid.UUID, user_connected: dict, db=None) -> Course:
        # Vérifier que l'utilisateur est bien un customer
        user_roles = (user_connected or {}).get("roles", [])
        if "customer" not in user_roles:
            raise ValueError("Seuls les customers peuvent annuler une course")

        # Récupérer la course
        course = self.getCourseById(course_id, db=db)
        if not course:
            raise ValueError("Course non trouvée")

        # Vérifier que la course est bien à l'état "demandée"
        if course.status != CourseStatus.DEMANDEE:
            raise ValueError("Seules les courses demandées peuvent être annulées")

        # Vérifier que l'utilisateur est bien le client de cette course
        if str(course.client_id) != user_connected.get("id"):
            raise ValueError("Vous ne pouvez annuler que vos propres courses")

        # Mettre à jour la course
        course.status = CourseStatus.ANNULEE
        course.updatedAt = datetime.utcnow()

        db.commit()
        db.refresh(course)
        return course

    @Database.with_session
    def startCourse(self, course_id: uuid.UUID, user_connected: dict, db=None) -> Course:
        # Vérifier que l'utilisateur est bien un driver
        user_roles = (user_connected or {}).get("roles", [])
        if "driver" not in user_roles:
            raise ValueError("Seuls les drivers peuvent démarrer une course")

        # Récupérer la course
        course = self.getCourseById(course_id, db=db)
        if not course:
            raise ValueError("Course non trouvée")

        # Vérifier que la course est bien à l'état "validée"
        if course.status != CourseStatus.VALIDEE:
            raise ValueError("Seules les courses validées peuvent être démarrées")

        # Vérifier que l'utilisateur est bien le chauffeur assigné à cette course
        if str(course.chauffeur_id) != user_connected.get("id"):
            raise ValueError("Vous ne pouvez démarrer que les courses qui vous sont assignées")

        # Mettre à jour la course
        course.status = CourseStatus.EN_COURS
        course.date_heure_depart = datetime.utcnow()
        course.updatedAt = datetime.utcnow()

        db.commit()
        db.refresh(course)
        return course

    def _calculate_fare(self, start_time: datetime, end_time: datetime) -> float:
        """
        Calcule le tarif de manière bidon pour le POC.
        Tarif de base: 5€ + 2€ par minute de course
        """
        # S'assurer que les deux datetime ont la même timezone (UTC)
        if start_time.tzinfo is not None and end_time.tzinfo is not None:
            # Les deux ont une timezone, on peut les soustraire directement
            duration = end_time - start_time
        else:
            # Au moins un des deux n'a pas de timezone, on les convertit en UTC
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=timezone.utc)
            if end_time.tzinfo is None:
                end_time = end_time.replace(tzinfo=timezone.utc)
            duration = end_time - start_time

        duration_minutes = duration.total_seconds() / 60

        base_fare = 5.0  # 5€ de prise en charge
        rate_per_minute = 2.0  # 2€ par minute

        total_fare = base_fare + (rate_per_minute * duration_minutes)

        # Arrondir à 2 décimales
        return round(total_fare, 2)

    @Database.with_session
    def endCourse(self, course_id: uuid.UUID, user_connected: dict, db=None) -> Course:
        # Vérifier que l'utilisateur est bien un driver
        user_roles = (user_connected or {}).get("roles", [])
        if "driver" not in user_roles:
            raise ValueError("Seuls les drivers peuvent terminer une course")

        # Récupérer la course
        course = self.getCourseById(course_id, db=db)
        if not course:
            raise ValueError("Course non trouvée")

        # Vérifier que la course est bien à l'état "en cours"
        if course.status != CourseStatus.EN_COURS:
            raise ValueError("Seules les courses en cours peuvent être terminées")

        # Vérifier que l'utilisateur est bien le chauffeur assigné à cette course
        if str(course.chauffeur_id) != user_connected.get("id"):
            raise ValueError("Vous ne pouvez terminer que les courses qui vous sont assignées")

        # Vérifier que la date de départ est renseignée
        if not course.date_heure_depart:
            raise ValueError("La course n'a pas de date de départ")

        # Mettre à jour la course
        course.status = CourseStatus.TERMINEE
        course.date_heure_arrivee = datetime.utcnow()
        course.updatedAt = datetime.utcnow()

        # Calculer le tarif en fonction de la durée (méthode bidon pour POC)
        course.tarif = self._calculate_fare(course.date_heure_depart, course.date_heure_arrivee)

        db.commit()
        db.refresh(course)
        return course

    @Database.with_session
    def getCoursesByClientId(self, client_id: uuid.UUID, db=None) -> list[Course]:
        return db.query(Course).filter(Course.client_id == client_id).order_by(Course.updatedAt.desc()).all()

    @Database.with_session
    def getCoursesByChauffeurId(self, chauffeur_id: uuid.UUID, db=None) -> list[Course]:
        return db.query(Course).filter(Course.chauffeur_id == chauffeur_id).order_by(Course.updatedAt.desc()).all()

    @Database.with_session
    def getMyCourses(self, user_connected: dict, db=None) -> list[Course]:
        user_id = user_connected.get("id")
        user_roles = user_connected.get("roles", [])

        if not user_id:
            raise ValueError("Utilisateur non identifié")

        user_uuid = uuid.UUID(user_id)

        if "customer" in user_roles:
            return self.getCoursesByClientId(user_uuid, db=db)

        if "driver" in user_roles:
            return self.getCoursesByChauffeurId(user_uuid, db=db)

        # Si l'utilisateur n'a aucun rôle pertinent
        else:
            raise ValueError("L'utilisateur doit avoir au moins un rôle customer ou driver")

    @Database.with_session
    def getPendingCourses(self, user_connected: dict, db=None) -> list[Course]:
        # Vérifier que l'utilisateur est bien un driver
        user_roles = (user_connected or {}).get("roles", [])
        if "driver" not in user_roles:
            raise ValueError("Seuls les drivers peuvent consulter les courses en attente")

        # Récupérer toutes les courses avec le statut "demandée"
        return db.query(Course).filter(
            Course.status == CourseStatus.DEMANDEE
        ).order_by(Course.updatedAt.desc()).all()

    @Database.with_session
    def deleteCourse(self, course_id: uuid.UUID, user_connected: dict, db=None) -> bool:
        # Vérifier que l'utilisateur est bien un admin
        user_roles = (user_connected or {}).get("roles", [])
        if "admin" not in user_roles:
            raise ValueError("Seuls les administrateurs peuvent supprimer une course")

        # Récupérer la course
        course = self.getCourseById(course_id, db=db)
        if not course:
            raise ValueError("Course non trouvée")

        # Supprimer la course
        db.delete(course)
        db.commit()

        return True

    