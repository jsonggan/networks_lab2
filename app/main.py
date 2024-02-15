from fastapi import FastAPI
from data import students

app = FastAPI()

@app.get("/")
def read_root():
    return "How are you?"

@app.get("/students/{student_id}")
def find_student(student_id: str):
    for student in students:
        if student["id"] == student_id:
            return student
    return None
