from fastapi import HTTPException

from app.command.CreateCourseCommand import CreateCourseCommand
from app.out.CourseOut import CourseOut
from app.repository.CourseRepository import CourseRepository


class CreateCourseUseCase:
    def __init__(self, command: CreateCourseCommand) -> None:
        self.command = command
        self.courseRepository = CourseRepository()

    def execute(self) -> CourseOut:
        try:
            entity = self.courseRepository.createCourse(self.command)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Erreur interne du serveur")

        return CourseOut.model_validate(entity)