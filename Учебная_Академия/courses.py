# Фёдоров Влад
from tkinter import ttk, messagebox, END
from database import добавить_курс, получить_все_курсы


class CourseManager:
    def __init__(self, master):
        self.master = master
        master.title("📚 Управление курсами")

        self.title_label = ttk.Label(master, text="Название:")
        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.title_entry = ttk.Entry(master, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        self.desc_label = ttk.Label(master, text="Описание:")
        self.desc_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.desc_entry = ttk.Entry(master, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(master, text="Добавить курс ➕", command=self.добавить_курс_gui)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.view_button = ttk.Button(master, text="Посмотреть все 👀", command=self.обновить_список)
        self.view_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

        self.tree = ttk.Treeview(master, columns=('ID', 'Название', 'Описание'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Название', text='Название')
        self.tree.heading('Описание', text='Описание')
        self.tree.column('ID', width=50, anchor='center')
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        master.grid_rowconfigure(4, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

        self.обновить_список()

    def добавить_курс_gui(self):
        название = self.title_entry.get().strip()
        описание = self.desc_entry.get().strip()
        if название:
            добавить_курс(название, описание)
            self.обновить_список()
            self.title_entry.delete(0, END)
            self.desc_entry.delete(0, END)
            messagebox.showinfo("✅ Успех", "Курс успешно добавлен!")
        else:
            messagebox.showwarning("⚠️ Предупреждение", "Введите название курса!")

    def обновить_список(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        курсы = получить_все_курсы()
        for курс in курсы:
            self.tree.insert('', 'end', values=курс)