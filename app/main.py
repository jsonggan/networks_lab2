from fastapi import FastAPI, Response, Header, Depends
from fastapi.responses import FileResponse
from typing import Optional
from db.db import setup_database
from model.student import Student
from controllers.student_controller import get_students, create_student, delete_student
from controllers.admin_controller import admin_home

app = FastAPI()

setup_database()

# Challenge 1: Return binary content types (image)
@app.get("/image")
def get_image():
    return FileResponse("sutd.jpeg")

# Challenge 2: Check bearer token in header
# verify that the bearer token is valid
@app.get("/admin/home")
def admin_verify(response: Response, authorization: Optional[str] = Header(None)):
    return admin_home(response, authorization)

# home route
@app.get("/")
def read_root():
    return {"message": "Welcome to simple rest api!"}

# get all students
# can sort by student id or gpa
# can limit the number of students to be returned
# default return message will sort by student id and limit list of students to 10
@app.get('/students')
def read_students(response: Response, sortBy: Optional[str] = None, limit: Optional[int] = None):
    return get_students(response, sortBy, limit)

# create a new student record
@app.post("/students")
def create_new_student(response: Response, student: Student):
    return create_student(response, student)

# delete a student record by student id
@app.delete("/students")
def delete_student_by_id(response: Response, student_id: int):
    return delete_student(response, student_id)