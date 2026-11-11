### Эмулятор командной строки ОС. Этап 1. ###
import getpass
import os
import socket


def get_prompt() -> str:
    # Формирует приглашение к вводу на основе реальных данных ОС
    username = getpass.getuser()
    hostname = socket.gethostname()
    cwd = os.getcwd()
    return f"{username}@{hostname}:{cwd}$ "


def main() -> None:
    # Запускает REPL (Read-Eval-Print Loop)
    print("Эмулятор запущен. Введите 'exit' для выхода.")
    
    while True:
        try:
            user_input = input(get_prompt())
        except (KeyboardInterrupt, EOFError):
            print("\nВыход.")
            break

        if not user_input.strip():
            continue
            
        if user_input.strip() == "exit":
            break

        # Раскрываем переменные окружения (например, $HOME)
        expanded_input = os.path.expandvars(user_input)
        parts = expanded_input.split()
        command = parts[0]
        args = parts[1:]

        # Заглушки
        if command in ("ls", "cd"):
            print(f"Заглушка: {command}, аргументы: {args}")
        else:
            print(f"Ошибка: неизвестная команда '{command}'")


if __name__ == "__main__":
    main()