from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from data import students
from typing import Optional
import sqlite3
from db.db import setup_database
from model.student import Student

app = FastAPI()
# Call the setup_database function to ensure the database is ready
db_path = "simple.db"

# Challenge 1: Return binary content types (image)
@app.get("/image")
def get_image():
    return FileResponse("sutd.jpeg")

@app.get("/")
def read_root():
    return {"message": "Welcome to simple rest api!"}

@app.get("/students/{student_id}")
def find_student(student_id: int, response: Response):
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
        if limit <= 0:
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

@app.delete("/students")
def delete_student(response: Response, student_id: int):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    if not student_id: 
        response.status_code = 422
        return {"message": "Please enter a student_id"}
    
    if student_id <= 0:
        response.status_code = 422
        return {'message': "student id must be a positive integer."}
    
    # Check if the student exist in the database
    cur.execute("SELECT * FROM student WHERE id = ?", (student_id,))
    if not cur.fetchone():
        con.close()
        response.status_code = 400
        return { "message": "Student doesn't exist"}
    
    # Delete the student record
    try:
        cur.execute("DELETE FROM student WHERE id = ?", (student_id,))
        con.commit()
    except sqlite3.Error as e:
        con.close()
        response.status_code = 422
        return {'message': f'Error when deleting record into database: {e}'}
    
    con.close()
    
    return {'message': 'successfully delete record from the database'}