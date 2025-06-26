# Михайлов Никита

from database import get_student_performance
from tkinter import ttk, messagebox, END
import tkinter as tk


class AnalyticsManager:
    def __init__(self, master):
        self.master = master
        master.title("📈 Аналитика успеваемости")

        self.course_id_label = ttk.Label(master, text="ID курса:")
        self.course_id_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.course_id_entry = ttk.Entry(master, width=30)
        self.course_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.students_button = ttk.Button(
            master, text="Список студентов на курсе 🧑‍🎓",
            command=self.show_students_on_course
        )
        self.students_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.average_button = ttk.Button(
            master, text="Средний балл по курсу 📈",
            command=self.show_average_grade
        )
        self.average_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.performance_button = ttk.Button(
            master, text="Успеваемость студентов 🌟",
            command=self.show_student_performance
        )
        self.performance_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.output_text = tk.Text(master, height=15, width=50)
        self.output_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        master.grid_rowconfigure(4, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

    def show_students_on_course(self):
        pass  # реализация зависит от другой функции из database.py

    def show_average_grade(self):
        pass  # реализация зависит от другой функции из database.py

    def show_student_performance(self):
        performance = get_student_performance()
        self.output_text.delete("1.0", END)
        if performance:
            self.output_text.insert(END, "🌟 Успеваемость студентов:\n")
            for name, avg in performance:
                self.output_text.insert(END, f"{name}: {avg:.2f}\n")
        else:
            self.output_text.insert(END, "❌ Нет данных.")
