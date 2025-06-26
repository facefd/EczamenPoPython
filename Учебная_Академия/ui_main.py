# Евсеенков Иван
import tkinter as tk
from tkinter import messagebox
from students import StudentManager
from courses import CourseManager
from instructors import InstructorManager
from enrollments import EnrollmentManager
from grades import GradeManager
from analytics import AnalyticsManager
from backup import BackupManager
from database import init_db


def open_window(manager_class):
    root = tk.Tk()
    app = manager_class(root)
    root.mainloop()


def main_menu():
    def on_closing():
        if messagebox.askokcancel("Выход", "Закрыть программу?"):
            root.destroy()

    root = tk.Tk()
    root.title("🎓 Учебная Академия — Главное меню")
    root.geometry("400x480")

    root.protocol("WM_DELETE_WINDOW", on_closing)

    tk.Label(root, text="🎓 Добро пожаловать в Учебную Академию!", font=("Arial", 14)).pack(pady=20)

    tk.Button(root, text="Управление студентами", width=30,
              command=lambda: [root.destroy(), open_window(StudentManager)]).pack(pady=5)

    tk.Button(root, text="Управление курсами", width=30,
              command=lambda: [root.destroy(), open_window(CourseManager)]).pack(pady=5)

    tk.Button(root, text="Управление преподавателями", width=30,
              command=lambda: [root.destroy(), open_window(InstructorManager)]).pack(pady=5)

    tk.Button(root, text="Запись на курсы", width=30,
              command=lambda: [root.destroy(), open_window(EnrollmentManager)]).pack(pady=5)

    tk.Button(root, text="Выставление оценок", width=30,
              command=lambda: [root.destroy(), open_window(GradeManager)]).pack(pady=5)

    tk.Button(root, text="Аналитика успеваемости", width=30,
              command=lambda: [root.destroy(), open_window(AnalyticsManager)]).pack(pady=5)

    tk.Button(root, text="Резервное копирование", width=30,
              command=lambda: [root.destroy(), open_window(BackupManager)]).pack(pady=5)

    tk.Button(root, text="Выйти из программы", width=30,
              command=root.destroy).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    init_db()
    main_menu()