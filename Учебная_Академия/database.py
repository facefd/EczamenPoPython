# Фёдоров Влад
import sqlite3

DB_NAME = "academyTop.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        tables = [
            """CREATE TABLE IF NOT EXISTS Студенты (
                id INTEGER PRIMARY KEY,
                имя TEXT NOT NULL,
                email TEXT UNIQUE
            )""",
            """CREATE TABLE IF NOT EXISTS Курсы (
                id INTEGER PRIMARY KEY,
                название TEXT NOT NULL,
                описание TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS Преподаватели (
                id INTEGER PRIMARY KEY,
                имя TEXT NOT NULL,
                email TEXT UNIQUE
            )""",
            """CREATE TABLE IF NOT EXISTS ЗаписиНаКурсы (
                id INTEGER PRIMARY KEY,
                id_студента INTEGER NOT NULL,
                id_курса INTEGER NOT NULL,
                FOREIGN KEY (id_студента) REFERENCES Студенты(id),
                FOREIGN KEY (id_курса) REFERENCES Курсы(id),
                UNIQUE(id_студента, id_курса)
            )""",
            """CREATE TABLE IF NOT EXISTS Оценки (
                id INTEGER PRIMARY KEY,
                id_записи INTEGER NOT NULL UNIQUE,
                оценка REAL NOT NULL CHECK(оценка >= 0 AND оценка <= 100),
                FOREIGN KEY (id_записи) REFERENCES ЗаписиНаКурсы(id)
            )"""
        ]

        for table in tables:
            cursor.execute(table)

        conn.commit()


# --- Студенты ---
def добавить_студента(имя, email):
    with connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Студенты (имя, email) VALUES (?, ?)", (имя, email))
        except sqlite3.IntegrityError:
            raise ValueError("Email уже существует")


def получить_всех_студентов():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, имя, email FROM Студенты")
        return cursor.fetchall()


def обновить_студента(student_id, имя, email):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Студенты SET имя=?, email=? WHERE id=?", (имя, email, student_id))


def удалить_студента(student_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Студенты WHERE id=?", (student_id,))


# --- Курсы ---
def добавить_курс(название, описание=None):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Курсы (название, описание) VALUES (?, ?)", (название, описание))


def получить_все_курсы():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, название, описание FROM Курсы")
        return cursor.fetchall()


# --- Преподаватели ---
def добавить_преподавателя(имя, email):
    with connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Преподаватели (имя, email) VALUES (?, ?)", (имя, email))
        except sqlite3.IntegrityError:
            raise ValueError("Email преподавателя уже занят")


def получить_всех_преподавателей():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, имя, email FROM Преподаватели")
        return cursor.fetchall()


# --- Записи на курсы ---
def добавить_запись(student_id, course_id):
    with connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO ЗаписиНаКурсы (id_студента, id_курса) VALUES (?, ?)",
                           (student_id, course_id))
        except sqlite3.IntegrityError:
            raise ValueError("Студент уже записан на этот курс")


def получить_всех_записей():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ЗаписиНаКурсы")
        return cursor.fetchall()


# --- Оценки ---
def выставить_оценку(enrollment_id, grade):
    with connect() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT OR REPLACE INTO Оценки (id_записи, оценка) VALUES (?, ?)",
                           (enrollment_id, grade))
        except sqlite3.IntegrityError:
            raise ValueError("Некорректная запись или оценка")


# --- Аналитика ---
def получить_среднюю_оценку_по_курсу(course_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AVG(o.оценка)
            FROM Оценки o
            JOIN ЗаписиНаКурсы z ON o.id_записи = z.id
            WHERE z.id_курса = ?
        """, (course_id,))
        result = cursor.fetchone()[0]
        return round(result, 2) if result else None


def получить_успеваемость_студентов():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.имя, AVG(o.оценка) AS avg_grade
            FROM Оценки o
            JOIN ЗаписиНаКурсы z ON o.id_записи = z.id
            JOIN Студенты s ON z.id_студента = s.id
            GROUP BY s.id, s.имя
        """)
        return cursor.fetchall()