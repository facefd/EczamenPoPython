# Новиков Никита
from tkinter import ttk, messagebox, END
from database import добавить_студента, получить_всех_студентов, обновить_студента, удалить_студента


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

        self.add_button = ttk.Button(master, text="Добавить студента ➕", command=self.добавить_студента)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.update_button = ttk.Button(master, text="Обновить данные 🔄", command=self.обновить_данные)
        self.update_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.delete_button = ttk.Button(master, text="Удалить студента 🗑️", command=self.удалить_студента)
        self.delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.view_button = ttk.Button(master, text="Посмотреть всех 👀", command=self.показать_всех)
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

        self.показать_всех()

    def добавить_студента(self):
        имя = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        if имя and email:
            try:
                добавить_студента(имя, email)
                self.показать_всех()
                self.name_entry.delete(0, END)
                self.email_entry.delete(0, END)
                messagebox.showinfo("✅ Успех", "Студент успешно добавлен!")
            except ValueError as e:
                messagebox.showerror("❌ Ошибка", str(e))
        else:
            messagebox.showwarning("⚠️ Предупреждение", "Заполните все поля!")

    def показать_всех(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        студенты = получить_всех_студентов()
        for student in студенты:
            self.tree.insert('', 'end', values=student)

    def выбрать_студента(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("❌ Ошибка", "Выберите студента")
            return None
        return self.tree.item(selected_item[0], 'values')

    def обновить_данные(self):
        студент = self.выбрать_студента()
        if студент:
            имя = self.name_entry.get().strip()
            email = self.email_entry.get().strip()
            if имя and email:
                обновить_студента(студент[0], имя, email)
                self.показать_всех()
                self.name_entry.delete(0, END)
                self.email_entry.delete(0, END)
                messagebox.showinfo("✅ Успех", "Данные студента обновлены!")
            else:
                messagebox.showwarning("⚠️ Предупреждение", "Заполните все поля!")

    def удалить_студента(self):
        студент = self.выбрать_студента()
        if студент:
            if messagebox.askyesno("Подтверждение", f"Удалить студента '{студент[1]}'?"):
                удалить_студента(студент[0])
                self.показать_всех()
                self.name_entry.delete(0, END)
                self.email_entry.delete(0, END)
                messagebox.showinfo("✅ Успех", "Студент удален!")