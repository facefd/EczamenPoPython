# Новиков никита
from tkinter import ttk, messagebox, END


class EnrollmentManager:
    def __init__(self, master):
        self.master = master
        master.title("📝 Регистрация на курсы")

        self.student_id_label = ttk.Label(master, text="ID студента:")
        self.student_id_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.student_id_entry = ttk.Entry(master, width=30)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.course_id_label = ttk.Label(master, text="ID курса:")
        self.course_id_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.course_id_entry = ttk.Entry(master, width=30)
        self.course_id_entry.grid(row=1, column=1, padx=5, pady=5)

        self.register_button = ttk.Button(master, text="Зарегистрировать ➕", command=self.зарегистрировать)
        self.register_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def зарегистрировать(self):
        try:
            student_id = int(self.student_id_entry.get())
            course_id = int(self.course_id_entry.get())
            from database import добавить_запись
            добавить_запись(student_id, course_id)
            self.student_id_entry.delete(0, END)
            self.course_id_entry.delete(0, END)
            messagebox.showinfo("✅ Успех", "Студент зарегистрирован на курс!")
        except ValueError as e:
            messagebox.showerror("❌ Ошибка", str(e))