import uuid
from fastapi import HTTPException

from app.command.DeleteCourseCommand import DeleteCourseCommand
from app.repository.CourseRepository import CourseRepository


class DeleteCourseUseCase:
    def __init__(self, course_id: uuid.UUID, command: DeleteCourseCommand) -> None:
        self.course_id = course_id
        self.command = command
        self.courseRepository = CourseRepository()

    def execute(self) -> dict:
        try:
            success = self.courseRepository.deleteCourse(self.course_id, self.command.userConnected or {})
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erreur interne du serveur")

        return {"deleted": success, "id": str(self.course_id)}
