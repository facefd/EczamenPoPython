# Михайлов Никита
from tkinter import ttk, messagebox, END


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
            command=self.показать_студентов_на_курсе
        )
        self.students_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.average_button = ttk.Button(
            master, text="Средний балл по курсу 📈",
            command=self.показать_средний_балл
        )
        self.average_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.performance_button = ttk.Button(
            master, text="Успеваемость студентов 🌟",
            command=self.показать_успеваемость
        )
        self.performance_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.output_text = tk.Text(master, height=15, width=50)
        self.output_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        master.grid_rowconfigure(4, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

    def показать_студентов_на_курсе(self):
        pass  # реализация зависит от другой функции из database.py

    def показать_средний_балл(self):
        pass  # реализация зависит от другой функции из database.py

    def показать_успеваемость(self):
        from database import получить_успеваемость_студентов
        успеваемость = получить_успеваемость_студентов()
        self.output_text.delete("1.0", END)
        if успеваемость:
            self.output_text.insert(END, "🌟 Успеваемость студентов:\n")
            for name, avg in успеваемость:
                self.output_text.insert(END, f"{name}: {avg:.2f}\n")
        else:
            self.output_text.insert(END, "❌ Нет данных.")