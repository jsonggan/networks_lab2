import sqlite3

# Path to the SQLite database
db_path = "simple.db"

def connect_db():
    # Connect to the SQLite database (this will create the database if it doesn't exist)
    con = sqlite3.connect(db_path)
    return con

def setup_database():
    con = connect_db()
    cur = con.cursor()

    # Check if the table already exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='student'")
    table_exists = cur.fetchone()

    # If the table does not exist, create it and insert data
    if not table_exists:
        cur.execute("CREATE TABLE student(id INTEGER, name TEXT, gpa REAL)")
        
        data = [
            (1006283, 'Gan Chin Song', 5.0),
            (1000000, 'Shelen Go', 4.31)
        ]
        
        cur.executemany("INSERT INTO student VALUES (?,?,?)", data)
        
        con.commit()
    else:
        print("Table 'student' already exists.")
    
    con.close()
