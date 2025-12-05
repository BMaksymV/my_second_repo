import logging
import os

class FileNotFound(Exception):
    """Файл не знайдено або файлу не існує"""
class FileCorrupted(Exception):
    """Файл пошкоджений або не підтримуваний формат"""

def logged(func):
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            log_file_path = os.path.join(os.getcwd(), "file_history.txt")
            handler = logging.FileHandler(log_file_path, encoding='utf-8')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        try:
            result = func(*args, **kwargs)
            logger.info(f"Успішно виконано: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Помилка у '{func.__name__}': {e}")
            raise
    return wrapper

class TextFileManager:
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(self.path):
            raise FileNotFound(f"Файл '{self.path}' не знайдено! Перевірте шлях.")

    @logged
    def read(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise FileCorrupted(f"Помилка читання: {e}")

    @logged
    def write(self, content: str):
        try:
            with open(self.path, 'w', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            raise FileCorrupted(f"Помилка запису: {e}")

    @logged
    def append(self, content: str):
        try:
            with open(self.path, 'a', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            raise FileCorrupted(f"Помилка дописування: {e}")

def menu():
    print("")
    print("    МЕНЮ ДІЙ")
    print("")
    print("1. Прочитати файл (Read)")
    print("2. Перезаписати файл (Write)")
    print("3. Дописати у файл (Append)")
    print("4. Змінити файл")
    print("exit. Вихід")
    print("")

def get_file_manager():
    while True:
        path = input("\nВведіть шлях до файлу (наприклад, my_notes.txt): ").strip()
        if not path:
            print("Шлях не може бути порожнім.")
            continue
            
        try:
            fm = TextFileManager(path)
            print(f"Успішно підключено до '{path}'")
            return fm
        except FileNotFound as e:
            print(f"Помилка: {e}")
            print("Спробуйте ввести інший шлях.")

if __name__ == "__main__":
    print("Program launched")
    print(f"Log path: {os.path.join(os.getcwd(), 'file_history.txt')}")
    
    manager = get_file_manager()

    while True:
        menu()
        choice = input("Ваш вибір: ").strip()

        try:
            if choice == "1":
                print("\n    ВМІСТ ФАЙЛУ    ")
                content = manager.read()
                print(content)

            elif choice == "2":
                text = input("Введіть текст для ЗАПИСУ (старий вміст видалиться): ")
                manager.write(text)
                print("Успішно записано.")

            elif choice == "3":
                text = input("Введіть текст для ДОПИСУВАННЯ (у кінець файлу): ")
                manager.append("\n" + text) 
                print("Успішно дописано.")

            elif choice == "4":
                manager = get_file_manager()

            elif choice == "exit":
                print("До побачення!")
                break
            
            else:
                print("Невірний вибір, спробуйте ще раз.")

        except FileCorrupted as e:
            print(f"\nОПЕРАЦІЯ НЕ ВДАЛАСЯ: {e}")
            print("(Деталі помилки записано у лог)")
        except Exception as e:
            print(f"\nНЕОЧІКУВАНА ПОМИЛКА: {e}")
