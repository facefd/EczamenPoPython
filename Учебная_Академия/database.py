# Фёдоров влад

import sqlite3

DB_NAME = "academyTOP.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        tables = [
            """CREATE TABLE IF NOT EXISTS Students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            )""",
            """CREATE TABLE IF NOT EXISTS Courses (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS Instructors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE
            )""",
            """CREATE TABLE IF NOT EXISTS Enrollments (
                id INTEGER PRIMARY KEY,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES Students(id),
                FOREIGN KEY (course_id) REFERENCES Courses(id),
                UNIQUE(student_id, course_id)
            )""",
            """CREATE TABLE IF NOT EXISTS Grades (
                id INTEGER PRIMARY KEY,
                enrollment_id INTEGER NOT NULL UNIQUE,
                grade REAL NOT NULL CHECK(grade >= 0 AND grade <= 100),
                FOREIGN KEY (enrollment_id) REFERENCES Enrollments(id)
            )"""
        ]

        for table in tables:
            cursor.execute(table)

        conn.commit()


# --- Students ---
def add_student(name, email):
    with connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", (name, email))
        except sqlite3.IntegrityError:
            raise ValueError("Email already exists")


def get_all_students():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM Students")
        return cursor.fetchall()


def update_student(student_id, name, email):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Students SET name=?, email=? WHERE id=?", (name, email, student_id))


def delete_student(student_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Students WHERE id=?", (student_id,))


# --- Courses ---
def add_course(title, description=None):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Courses (title, description) VALUES (?, ?)", (title, description))


def get_all_courses():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description FROM Courses")
        return cursor.fetchall()


# --- Instructors ---
def add_instructor(name, email):
    with connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Instructors (name, email) VALUES (?, ?)", (name, email))
        except sqlite3.IntegrityError:
            raise ValueError("Instructor's email is already taken")


def get_all_instructors():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM Instructors")
        return cursor.fetchall()


# --- Enrollments ---
def add_enrollment(student_id, course_id):
    with connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Enrollments (student_id, course_id) VALUES (?, ?)",
                           (student_id, course_id))
        except sqlite3.IntegrityError:
            raise ValueError("Student is already enrolled in this course")


def get_all_enrollments():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Enrollments")
        return cursor.fetchall()


# --- Grades ---
def set_grade(enrollment_id, grade):
    with connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT OR REPLACE INTO Grades (enrollment_id, grade) VALUES (?, ?)",
                           (enrollment_id, grade))
        except sqlite3.IntegrityError:
            raise ValueError("Invalid enrollment or grade")


# --- Analytics ---
def get_average_grade_by_course(course_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AVG(g.grade)
            FROM Grades g
            JOIN Enrollments e ON g.enrollment_id = e.id
            WHERE e.course_id = ?
        """, (course_id,))
        result = cursor.fetchone()[0]
        return round(result, 2) if result else None


def get_student_performance():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.name, AVG(g.grade) AS avg_grade
            FROM Grades g
            JOIN Enrollments e ON g.enrollment_id = e.id
            JOIN Students s ON e.student_id = s.id
            GROUP BY s.id, s.name
        """)
        return cursor.fetchall()
