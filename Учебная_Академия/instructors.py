# Михайлов Никита
from tkinter import ttk, messagebox, END
from database import add_instructor, get_all_instructors


class InstructorManager:
    def __init__(self, master):
        self.master = master
        master.title("🧑‍🏫 Управление преподавателями")

        self.name_label = ttk.Label(master, text="Имя:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.name_entry = ttk.Entry(master, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.email_label = ttk.Label(master, text="Email:")
        self.email_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.email_entry = ttk.Entry(master, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(master, text="Добавить преподавателя ➕", command=self.add_instructor_gui)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.view_button = ttk.Button(master, text="Посмотреть всех 👀", command=self.show_all_instructors)
        self.view_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.tree = ttk.Treeview(master, columns=('ID', 'Имя', 'Email'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Имя', text='Имя')
        self.tree.heading('Email', text='Email')
        self.tree.column('ID', width=50, anchor='center')
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        master.grid_rowconfigure(4, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

        self.show_all_instructors()

    def add_instructor_gui(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        if name and email:
            try:
                add_instructor(name, email)
                self.show_all_instructors()
                self.name_entry.delete(0, END)
                self.email_entry.delete(0, END)
                messagebox.showinfo("✅ Успех", "Преподаватель успешно добавлен!")
            except ValueError as e:
                messagebox.showerror("❌ Ошибка", str(e))
        else:
            messagebox.showwarning("⚠️ Предупреждение", "Заполните все поля!")

    def show_all_instructors(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        instructors = get_all_instructors()
        for instr in instructors:
            self.tree.insert('', 'end', values=instr)
