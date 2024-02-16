from fastapi import FastAPI, Response
from data import students
from typing import Optional
import sqlite3
from db.db import setup_database


app = FastAPI()
# Call the setup_database function to ensure the database is ready
db_path = "simple.db"

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
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # TODO: if parameters are not None, sort & limit...
    query = "SELECT * FROM student"
    # TODO: validate the sortBy value, can only be id and gpa
    if sortBy in ['id', 'gpq']:
        query += f" ORDER BY {sortBy}"
    # TODO: validate the count value, it should only be integer and cannot be a non positive value
    if limit:
        query += f" LIMIT {limit}"
        
    cur.execute(query)
    students = cur.fetchall()
    
    student_list = [{
        'id': student[0],
        'name': student[1],
        'gpa': student[2] 
    } for student in students]
    
    con.close()
    
    return student_list