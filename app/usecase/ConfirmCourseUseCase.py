import uuid
from fastapi import HTTPException

from app.command.ConfirmCourseCommand import ConfirmCourseCommand
from app.out.CourseOut import CourseOut
from app.repository.CourseRepository import CourseRepository


class ConfirmCourseUseCase:
    def __init__(self, course_id: uuid.UUID, command: ConfirmCourseCommand) -> None:
        self.course_id = course_id
        self.command = command
        self.courseRepository = CourseRepository()

    def execute(self) -> CourseOut:
        try:
            entity = self.courseRepository.confirmCourse(self.course_id, self.command.userConnected or {})
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erreur interne du serveur")

        return CourseOut.model_validate(entity)