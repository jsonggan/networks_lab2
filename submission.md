# FastAPI Students Application

This FastAPI application provides a RESTful API to manage student records, including retrieving student details, adding new students, and deleting students based on their ID.

## Getting Started

run `docker compose up` to run the application

## Making HTTP Requests

Please use the provided "Lab 2 network.postman_collection.json" for checking purpose.

1. Retrieve All Students
   GET /students
   Optional Query Parameters: sortBy (id, gpa), limit (integer).  
   Expected Response: A list of students, optionally sorted and limited.

2. Add a New Student
   POST /students
   Body:  
   json  
   {  
   "id": int,  
   "name": "string",  
   "gpa": float  
   }  
   Expected Response: Confirmation message with the created student's details.

3. Delete a Student  
   DELETE /students  
   Query Parameter: student_id (integer)  
   Expected Response: Confirmation message of deletion.

4. Get an image  
   GET /image  
   Get a SUTD logo jpeg image

5. Enter admin home  
   GET /admin/home  
   Bearer token: Oo9mzIKFlWiP8JTblDFTc886ysXHexuHADVqU5RMcifjJpyXEOuxP0TIdgQOiVeJ  
   return "welcome admin!" if provide a valid token  
   return unverified if provide a non-valid token

## Idempotency

GET /students is idempotent as it retrieves information without changing the server's state.  
DELETE /students is idempotent as deleting the same resource multiple times will have the same effect as deleting it once; subsequent requests will simply return a not found response.

### Proof of Idempotency

Repeated GET requests for the same student_id return the same student data, proving idempotency.  
A DELETE request for a specific student_id will succeed the first time and either fail or return a not found message on subsequent attempts, proving idempotency.
