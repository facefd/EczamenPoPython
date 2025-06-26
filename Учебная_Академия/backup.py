# Фёдоров Влад
from tkinter import ttk, messagebox, filedialog, END, Text
import sqlite3
import shutil
import os
import datetime


class BackupManager:
    def __init__(self, master):
        self.master = master
        master.title("📦 Резервное копирование")

        # Кнопки
        self.backup_button = ttk.Button(
            master, text="Создать резервную копию 💾", command=self.create_backup
        )
        self.backup_button.pack(pady=10, padx=10, fill='x')

        self.restore_button = ttk.Button(
            master, text="Восстановить из копии 🔁", command=self.restore_from_backup
        )
        self.restore_button.pack(pady=10, padx=10, fill='x')

        # Лог
        self.log_text = Text(master, height=15, width=50)
        self.log_text.pack(pady=10, padx=10, fill='both', expand=True)

        self.add_log("📚 Готов к работе")

    def create_backup(self):
        original_file = "academyTOP.db"  # ✅ Правильное имя БД

        if not os.path.exists(original_file):
            self.add_log("❌ Основной файл не найден")
            return

        backup_folder = "backups"
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)

        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"academyTOP_backup_{current_time}.db"
        backup_path = os.path.join(backup_folder, backup_name)

        try:
            shutil.copy2(original_file, backup_path)
            self.add_log(f"✅ Сохранено: {backup_path}")
        except Exception as e:
            self.add_log(f"❌ Ошибка при создании бэкапа: {e}")

    def restore_from_backup(self):
        backup_folder = "backups"
        if not os.path.exists(backup_folder):
            self.add_log("❌ Папка backups не найдена")
            return

        selected_file = filedialog.askopenfilename(
            initialdir=backup_folder,
            title="Выберите бэкап",
            filetypes=[("SQLite DB", "*.db")]
        )
        if not selected_file:
            return

        original_file = "academyTOP.db"

        try:
            # Закрываем соединение с БД, если оно есть
            conn = sqlite3.connect(original_file)
            conn.execute("PRAGMA busy_timeout = 3000")
            conn.close()

            # Перезаписываем основной файл
            shutil.copy2(selected_file, original_file)
            self.add_log(f"✅ Восстановлено: {selected_file}")
            messagebox.showinfo("✅ Успех", "База данных успешно восстановлена.")
        except Exception as e:
            messagebox.showerror("❌ Ошибка", f"Не удалось восстановить: {str(e)}")
            self.add_log(f"❌ Ошибка при восстановлении: {e}")

    def add_log(self, message):
        self.log_text.insert(END, f"{message}\n")
        self.log_text.see(END)
