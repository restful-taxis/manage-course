import uuid

from fastapi import FastAPI, Depends
import app.models  # Assure le chargement des modèles

from app.service.Auth import Auth

from app.command.CancelCourseCommand import CancelCourseCommand
from app.command.ConfirmCourseCommand import ConfirmCourseCommand
from app.command.CreateCourseCommand import CreateCourseCommand
from app.command.EndCourseCommand import EndCourseCommand
from app.command.GetMyCoursesCommand import GetMyCoursesCommand
from app.command.GetPendingCoursesCommand import GetPendingCoursesCommand
from app.command.StartCourseCommand import StartCourseCommand

from app.usecase.CancelCourseUseCase import CancelCourseUseCase
from app.usecase.ConfirmCourseUseCase import ConfirmCourseUseCase
from app.usecase.CreateCourseUseCase import CreateCourseUseCase
from app.usecase.EndCourseUseCase import EndCourseUseCase
from app.usecase.GetMyCoursesUseCase import GetMyCoursesUseCase
from app.usecase.GetPendingCoursesUseCase import GetPendingCoursesUseCase
from app.usecase.StartCourseUseCase import StartCourseUseCase

app = FastAPI(title="Course Microservice")
auth = Auth()

@app.post("/create")
def create_course(command: CreateCourseCommand, currentUser = Depends(auth.getCurrentUser)):
    command.userConnected = currentUser
    useCase = CreateCourseUseCase(command)
    return useCase.execute()

@app.post("/{course_id}/confirm")
def confirm_course(course_id: uuid.UUID, command: ConfirmCourseCommand, currentUser = Depends(auth.getCurrentUser)):
    command.userConnected = currentUser
    useCase = ConfirmCourseUseCase(course_id, command)
    return useCase.execute()

@app.post("/{course_id}/cancel")
def cancel_course(course_id: uuid.UUID, command: CancelCourseCommand, currentUser = Depends(auth.getCurrentUser)):
    command.userConnected = currentUser
    useCase = CancelCourseUseCase(course_id, command)
    return useCase.execute()

@app.post("/{course_id}/start")
def start_course(course_id: uuid.UUID, command: StartCourseCommand, currentUser = Depends(auth.getCurrentUser)):
    command.userConnected = currentUser
    useCase = StartCourseUseCase(course_id, command)
    return useCase.execute()

@app.post("/{course_id}/end")
def end_course(course_id: uuid.UUID, command: EndCourseCommand, currentUser = Depends(auth.getCurrentUser)):
    command.userConnected = currentUser
    useCase = EndCourseUseCase(course_id, command)
    return useCase.execute()

@app.get("/my")
def get_my_courses(currentUser = Depends(auth.getCurrentUser)):
    command = GetMyCoursesCommand(userConnected=currentUser)
    useCase = GetMyCoursesUseCase(command)
    return useCase.execute()

@app.get("/pending")
def get_pending_courses(currentUser = Depends(auth.getCurrentUser)):
    command = GetPendingCoursesCommand(userConnected=currentUser)
    useCase = GetPendingCoursesUseCase(command)
    return useCase.execute()
