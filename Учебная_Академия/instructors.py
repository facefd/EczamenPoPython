# Михайлов Никита
from tkinter import ttk, messagebox, END
from database import добавить_преподавателя, получить_всех_преподавателей


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

        self.add_button = ttk.Button(master, text="Добавить преподавателя ➕", command=self.добавить_преподавателя)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.view_button = ttk.Button(master, text="Посмотреть всех 👀", command=self.показать_всех)
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

        self.показать_всех()

    def добавить_преподавателя(self):
        имя = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        if имя and email:
            try:
                добавить_преподавателя(имя, email)
                self.показать_всех()
                self.name_entry.delete(0, END)
                self.email_entry.delete(0, END)
                messagebox.showinfo("✅ Успех", "Преподаватель успешно добавлен!")
            except ValueError as e:
                messagebox.showerror("❌ Ошибка", str(e))
        else:
            messagebox.showwarning("⚠️ Предупреждение", "Заполните все поля!")

    def показать_всех(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        преподаватели = получить_всех_преподавателей()
        for instr in преподаватели:
            self.tree.insert('', 'end', values=instr)