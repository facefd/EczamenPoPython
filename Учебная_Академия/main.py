#Гайдин Артём и компановка

from ui_main import main_menu
from database import (
    add_student,
    get_all_courses,
    add_enrollment,
    set_grade,
    get_student_performance,
)


def cli_menu():
    while True:
        print("\n🎓 АКАДЕМИЯ — Главное меню")
        print("1. Добавить студента")
        print("2. Посмотреть курсы")
        print("3. Записать на курс")
        print("4. Поставить оценку")
        print("5. Показать аналитику успеваемости")
        print("6. Выйти")

        выбор = input("Выберите действие: ").strip()

        if выбор == "1":
            имя = input("Введите имя студента: ").strip()
            email = input("Введите email студента: ").strip()
            try:
                add_student(имя, email)
                print(f"✅ Студент {имя} успешно добавлен.")
            except ValueError as e:
                print(f"❌ Ошибка: {e}")

        elif выбор == "2":
            курсы = get_all_courses()
            print("\n📚 Список курсов:")
            for курс in курсы:
                print(f"ID: {курс[0]}, Название: {курс[1]}, Описание: {курс[2]}")

        elif выбор == "3":
            try:
                student_id = int(input("Введите ID студента: "))
                course_id = int(input("Введите ID курса: "))
                add_enrollment(student_id, course_id)
                print(f"✅ Студент с ID {student_id} записан на курс с ID {course_id}.")
            except ValueError as e:
                print(f"❌ Ошибка: {e}")
            except Exception as e:
                print(f"⚠️ Неожиданная ошибка: {e}")

        elif выбор == "4":
            try:
                enrollment_id = int(input("Введите ID записи: "))
                grade = float(input("Введите оценку (от 0 до 100): "))
                if 0 <= grade <= 100:
                    set_grade(enrollment_id, grade)
                    print(f"✅ Оценка {grade} успешно выставлена.")
                else:
                    print("❌ Оценка должна быть от 0 до 100!")
            except ValueError:
                print("❌ Некорректный ввод!")

        elif выбор == "5":
            успеваемость = get_student_performance()
            print("\n🌟 Успеваемость студентов:")
            if успеваемость:
                for name, avg in успеваемость:
                    print(f"{name}: {avg:.2f}")
            else:
                print("❌ Нет данных.")

        elif выбор == "6":
            print("👋 До свидания!")
            break

        else:
            print("⚠️ Неправильный выбор. Попробуйте снова.")


if __name__ == "__main__":
    print("🌐 Запуск программы...")
    print("1. Графический интерфейс")
    print("2. Консольный интерфейс (CLI)")
    режим = input("Выберите режим работы (1 или 2): ").strip()

    if режим == "1":
        main_menu()
    elif режим == "2":
        cli_menu()
    else:
        print("❌ Некорректный режим. Завершение работы.")
