import logging
import os

class FileNotFound(Exception):
    """File isnt exist"""
class FileCorrupted(Exception):
    """File is damaged or not supported"""

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
            logger.info(f"Successfully completed: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error in '{func.__name__}': {e}")
            raise
    return wrapper

class TextFileManager:
    def __init__(self, path: str):
        self.path = path
        if not os.path.exists(self.path):
            raise FileNotFound(f"File '{self.path}' isnt found! check path.")

    @logged
    def read(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise FileCorrupted(f"Read error: {e}")

    @logged
    def write(self, content: str):
        try:
            with open(self.path, 'w', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            raise FileCorrupted(f"Rewriting error: {e}")

    @logged
    def append(self, content: str):
        try:
            with open(self.path, 'a', encoding='utf-8') as file:
                file.write(content)
        except Exception as e:
            raise FileCorrupted(f"Adding error: {e}")

def menu():
    print("\n    ACTION MENU \n \n 1. Read file \n 2. Rewrite file \n 3. Add to file \n 4. Change file/file path \n 5. Exit\n")

def get_file_manager():
    while True:
        path = input("\n Enter file path (example, my_notes.txt): ").strip()
        if not path:
            print("File path shouldnt be empty")
            continue
            
        try:
            fm = TextFileManager(path)
            print(f"Successfully connected to '{path}'")
            return fm
        except FileNotFound as e:
            print(f"Error: {e}")
            print("Try enter other file path.")

if __name__ == "__main__":
    print("Program launched")
    print(f"Log path: {os.path.join(os.getcwd(), 'file_history.txt')}")
    
    manager = get_file_manager()

    while True:
        menu()
        choice = input("Your choice: ").strip()

        try:
            if choice == "1":
                print("\n    FILE CONTENTS    ")
                content = manager.read()
                print(content)

            elif choice == "2":
                text = input("Enter text for RECORD (old content will be deleted): ")
                manager.write(text)
                print("Successfully recorded.")

            elif choice == "3":
                text = input("Enter text for ADDing (at the end of the file): ")
                manager.append("\n" + text) 
                print("Successfully recorded.")

            elif choice == "4":
                manager = get_file_manager()

            elif choice == "exit":
                print("Bye!")
                break
            
            else:
                print("Wrong choice , try again")

        except FileCorrupted as e:
            print(f"\n OPERATION FAILED: {e}")
            print("(Error details are recorded in the log.)")
        except Exception as e:
            print(f"\n UNEXPECTED ERROR: {e}")

