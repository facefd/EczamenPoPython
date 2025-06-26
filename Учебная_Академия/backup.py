# Фёдоров Влад
from tkinter import ttk, messagebox, filedialog, END
import sqlite3
import shutil
import os
import datetime


class BackupManager:
    def __init__(self, master):
        self.master = master
        master.title("📦 Резервное копирование")

        self.backup_button = ttk.Button(master, text="Создать резервную копию 💾", command=self.сделать_бэкап)
        self.backup_button.pack(pady=10, padx=10, fill='x')

        self.restore_button = ttk.Button(master, text="Восстановить из копии 🔁", command=self.восстановить_из_копии)
        self.restore_button.pack(pady=10, padx=10, fill='x')

        self.log_text = tk.Text(master, height=15, width=50)
        self.log_text.pack(pady=10, padx=10, fill='both', expand=True)

        self.добавить_лог("📚 Готов к работе")

    def сделать_бэкап(self):
        оригинальный_файл = 'school.db'
        if not os.path.exists(оригинальный_файл):
            self.добавить_лог("❌ Основной файл не найден")
            return

        папка_бэкапов = 'backups'
        if not os.path.exists(папка_бэкапов):
            os.makedirs(папка_бэкапов)

        текущее_время = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        имя_копии = f"school_backup_{текущее_время}.db"
        путь_копии = os.path.join(папка_бэкапов, имя_копии)

        try:
            shutil.copy2(оригинальный_файл, путь_копии)
            self.добавить_лог(f"✅ Сохранено: {путь_копии}")
        except Exception as e:
            self.добавить_лог(f"❌ Ошибка: {e}")

    def восстановить_из_копии(self):
        папка_бэкапов = 'backups'
        if not os.path.exists(папка_бэкапов):
            self.добавить_лог("❌ Папка backups не найдена")
            return

        файл = filedialog.askopenfilename(
            initialdir=папка_бэкапов,
            title="Выберите бэкап",
            filetypes=[("SQLite DB", "*.db")]
        )
        if not файл:
            return

        try:
            sqlite3.connect('school.db').close()
            shutil.copy2(файл, 'school.db')
            self.добавить_лог(f"✅ Восстановлено: {файл}")
        except Exception as e:
            self.добавить_лог(f"❌ Ошибка: {e}")

    def добавить_лог(self, сообщение):
        self.log_text.insert("end", f"{сообщение}\n")
        self.log_text.see("end")