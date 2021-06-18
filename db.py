import sqlite3

def database():
    conn = sqlite3.connect("./grades.db")
    cursor = conn.cursor()
    query = """ CREATE TABLE IF NOT EXISTS 'grades' (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    studentEnrollment INTEGER NOT NULL,
                    studentName TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    grade1 REAL NOT NULL,
                    grade2 REAL NOT NULL,
                    grade3 REAL NOT NULL,
                    gradeAvd REAL NOT NULL,
                    gradeAvds REAL NOT NULL,
                    average REAL NOT NULL,
                    situation INTEGER NOT NULL
                )
            """
    cursor.execute(query)
    cursor.execute("SELECT studentEnrollment, studentName, subject, grade1, grade2, grade3, gradeAvd, gradeAvds, average, situation FROM 'grades' ORDER BY subject")
    fetch = cursor.fetchall()

    return fetch

def insert(studentEnrollment, studentName, subject, grade1, grade2, grade3, gradeAvd, gradeAvds, average, situation):
    conn = sqlite3.connect("./grades.db")
    cursor = conn.cursor()
    query = """ INSERT INTO 'grades' (studentEnrollment, studentName, subject, grade1, grade2, grade3, gradeAvd, gradeAvds, average, situation) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(
        query, 
        (
            studentEnrollment,
            studentName, 
            subject, 
            grade1, 
            grade2,
            grade3,
            gradeAvd,
            gradeAvds,
            average,
            situation
        )
    )
    
    
    conn.commit()

    cursor.execute("SELECT studentEnrollment, studentName, subject, grade1, grade2, grade3, gradeAvd, gradeAvds, average, situation FROM 'grades' ORDER BY subject")
    fetch = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return fetch

def delete(studentEnrollment, subjectItem):
    conn = sqlite3.connect("./grades.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM 'grades' WHERE studentEnrollment = %d AND subject = '%s'" % (studentEnrollment, subjectItem))
    
    conn.commit()
    cursor.close()
    conn.close()

def update(studentEnrollment, studentName, subject, grade1, grade2, grade3, gradeAvd, gradeAvds, average, situation):
    conn = sqlite3.connect("./grades.db")
    cursor = conn.cursor()
    cursor.execute("""UPDATE 'grades' SET studentEnrollment=?, studentName=?, subject=?, grade1=?, grade2=?, grade3=?, gradeAvd=?, gradeAvds=?, average=?, situation=? WHERE studentEnrollment=? AND subject=?""", (studentEnrollment, studentName, subject, grade1, grade2, grade3, gradeAvd, gradeAvds, average, situation, studentEnrollment, subject))

    conn.commit()

    cursor.execute("SELECT studentEnrollment, studentName, subject, grade1, grade2, grade3, gradeAvd, gradeAvds, average, situation FROM 'grades' ORDER BY subject")
    fetch = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return fetch

def select(studentEnrollment, subjectItem):
    conn = sqlite3.connect("./grades.db")
    cursor = conn.cursor()
    cursor.execute("SELECT studentEnrollment, studentName, subject, grade1, grade2, grade3, gradeAvd, gradeAvds, average, situation FROM 'grades' WHERE studentEnrollment = %d AND subject = '%s'" % (studentEnrollment, subjectItem))

    fetch = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return fetch