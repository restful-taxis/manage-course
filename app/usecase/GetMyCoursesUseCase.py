from fastapi import HTTPException

from app.command.GetMyCoursesCommand import GetMyCoursesCommand
from app.out.CourseOut import CourseOut
from app.repository.CourseRepository import CourseRepository


class GetMyCoursesUseCase:
    def __init__(self, command: GetMyCoursesCommand) -> None:
        self.command = command
        self.courseRepository = CourseRepository()

    def execute(self) -> list[CourseOut]:
        try:
            entities = self.courseRepository.getMyCourses(self.command.userConnected or {})
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erreur interne du serveur")

        return [CourseOut.model_validate(entity) for entity in entities]