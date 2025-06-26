# Новиков Никита
from tkinter import ttk, messagebox, END
from database import set_grade


class GradeManager:
    def __init__(self, master):
        self.master = master
        master.title("📊 Выставление оценок")

        self.enrollment_id_label = ttk.Label(master, text="ID записи:")
        self.enrollment_id_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.enrollment_id_entry = ttk.Entry(master, width=30)
        self.enrollment_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.grade_label = ttk.Label(master, text="Оценка (0–100):")
        self.grade_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.grade_entry = ttk.Entry(master, width=30)
        self.grade_entry.grid(row=1, column=1, padx=5, pady=5)

        self.set_grade_button = ttk.Button(master, text="Выставить оценку ✅", command=self.set_grade_gui)
        self.set_grade_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def set_grade_gui(self):
        try:
            eid = int(self.enrollment_id_entry.get())
            grade = float(self.grade_entry.get())
            if 0 <= grade <= 100:
                set_grade(eid, grade)
                self.enrollment_id_entry.delete(0, END)
                self.grade_entry.delete(0, END)
                messagebox.showinfo("✅ Успех", "Оценка выставлена!")
            else:
                messagebox.showwarning("⚠️ Предупреждение", "Оценка должна быть от 0 до 100")
        except ValueError:
            messagebox.showerror("❌ Ошибка", "Некорректные данные!")
