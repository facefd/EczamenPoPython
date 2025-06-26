# Новиков Никита

from tkinter import ttk, messagebox, END
from database import add_student, get_all_students, update_student, delete_student


class StudentManager:
    def __init__(self, master):
        self.master = master
        master.title("🎓 Управление студентами")

        self.name_label = ttk.Label(master, text="Имя:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.name_entry = ttk.Entry(master, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.email_label = ttk.Label(master, text="Email:")
        self.email_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.email_entry = ttk.Entry(master, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(master, text="Добавить студента ➕", command=self.add_student_gui)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.update_button = ttk.Button(master, text="Обновить данные 🔄", command=self.update_student_gui)
        self.update_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.delete_button = ttk.Button(master, text="Удалить студента 🗑️", command=self.delete_student_gui)
        self.delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.view_button = ttk.Button(master, text="Посмотреть всех 👀", command=self.show_all_students)
        self.view_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.tree = ttk.Treeview(master, columns=('ID', 'Имя', 'Email'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Имя', text='Имя')
        self.tree.heading('Email', text='Email')
        self.tree.column('ID', width=50, anchor='center')
        self.tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        master.grid_rowconfigure(6, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

        self.show_all_students()

    def add_student_gui(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        if name and email:
            try:
                add_student(name, email)
                self.show_all_students()
                self.name_entry.delete(0, END)
                self.email_entry.delete(0, END)
                messagebox.showinfo("✅ Успех", "Студент успешно добавлен!")
            except ValueError as e:
                messagebox.showerror("❌ Ошибка", str(e))
        else:
            messagebox.showwarning("⚠️ Предупреждение", "Заполните все поля!")

    def show_all_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        students = get_all_students()
        for student in students:
            self.tree.insert('', 'end', values=student)

    def select_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("❌ Ошибка", "Выберите студента")
            return None
        return self.tree.item(selected_item[0], 'values')

    def update_student_gui(self):
        student = self.select_student()
        if student:
            name = self.name_entry.get().strip()
            email = self.email_entry.get().strip()
            if name and email:
                update_student(student[0], name, email)
                self.show_all_students()
                self.name_entry.delete(0, END)
                self.email_entry.delete(0, END)
                messagebox.showinfo("✅ Успех", "Данные студента обновлены!")
            else:
                messagebox.showwarning("⚠️ Предупреждение", "Заполните все поля!")

    def delete_student_gui(self):
        student = self.select_student()
        if student:
            if messagebox.askyesno("Подтверждение", f"Удалить студента '{student[1]}'?"):
                delete_student(student[0])
                self.show_all_students()
                self.name_entry.delete(0, END)
                self.email_entry.delete(0, END)
                messagebox.showinfo("✅ Успех", "Студент удален!")
