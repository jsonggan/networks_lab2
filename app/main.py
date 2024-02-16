from fastapi import FastAPI, Response
from data import students
from typing import Optional
import sqlite3
from db.db import setup_database
from model.student import Student

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
def get_students(response: Response, sortBy: Optional[str] = None, limit: Optional[int] = None):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    query = "SELECT * FROM student"
    
    if sortBy:
        if sortBy not in ['id', 'gpa']:
            response.status_code = 422
            return { 'message': "sortBy can only receive id and gpa"}
        query += f" ORDER BY {sortBy}"
        
    if limit:
        try:
            limit = int(limit)
            if limit <= 0:
                raise ValueError
        except ValueError:
            response.status_code = 422
            return {'message': "limit must be a positive integer."}
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

@app.post("/students")
def create_student(response: Response, student: Student):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    # Check if the student already exists to avoid duplicates
    cur.execute("SELECT * FROM student WHERE id = ?", (student.id,))
    if cur.fetchone():
        con.close()
        response.status_code = 400
        return { "message": "Student already existed"}

    # Insert new student into the database
    try:
        cur.execute("INSERT INTO student (id, name, gpa) VALUES (?, ?, ?)", (student.id, student.name, student.gpa))
        con.commit()
    except sqlite3.Error as e:
        con.close()
        response.status_code = 422
        return {'message': f'Error when inserting record into database: {e}'}
    
    con.close()
    
    return {'message': 'successfully insert record into database'}