from fastapi import FastAPI, Response
from data import students
from typing import Optional
import sqlite3

data = [ (1006283, 'Gan Chin Song', 5.0), (1000000, 'Shelen Go', '4.31')]

con = sqlite3.connect("simple.db")
cur = con.cursor() # database cursor
cur.execute("CREATE TABLE student(id, name, gpa)")
cur.executemany("INSERT INTO student VALUES (?,?,?)", data)
con.commit()

app = FastAPI()

@app.get("/")
def read_root():
    return "How are you?"

@app.get("/students/{student_id}")
def find_student(student_id: str, response: Response):
    for student in students:
        if student["id"] == student_id:
            return student
    response.status_code = 400
    return None

@app.get('/students')
def get_students(sortBy: Optional[str] = None, limit: Optional[int] = None):
    # TODO: if parameters are not None, sort & limit...
    return {"message" : "correct"}