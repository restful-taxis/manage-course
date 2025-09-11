from fastapi import HTTPException

from app.command.GetPendingCoursesCommand import GetPendingCoursesCommand
from app.out.CourseOut import CourseOut
from app.repository.CourseRepository import CourseRepository


class GetPendingCoursesUseCase:
    def __init__(self, command: GetPendingCoursesCommand) -> None:
        self.command = command
        self.courseRepository = CourseRepository()

    def execute(self) -> list[CourseOut]:
        try:
            entities = self.courseRepository.getPendingCourses(self.command.userConnected or {})
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erreur interne du serveur")

        return [CourseOut.model_validate(entity) for entity in entities]