### Точка входа эмулятора командной строки (Вариант 15) ###
import argparse
import os

from src.commands import ShellState
from src.repl import execute_command, repl
from src.vfs import load_vfs


def run_script(state: ShellState, script_path: str) -> None:
    # Выполняет стартовый скрипт с остановкой при первой ошибке
    if not os.path.isfile(script_path):
        print(f"Ошибка: файл скрипта не найден: {script_path}")
        return

    print(f"--- Выполнение скрипта: {script_path} ---")
    with open(script_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            # Показываем "ввод" пользователя (требование этапа 2)
            print(f"Эмулятор> {line}")
            
            # Если команда вернула False (exit или ошибка) — останавливаем скрипт.
            if not execute_command(state, line):
                print("Скрипт остановлен.")
                break
    print("--- Скрипт завершен ---")


def main() -> None:
    # Главная функция: разбор аргументов, загрузка VFS, запуск
    parser = argparse.ArgumentParser(description="Эмулятор Shell (Вариант 15)")
    parser.add_argument("--vfs-path", help="Путь к директории VFS на диске")
    parser.add_argument("--script", help="Путь к стартовому скрипту")
    args = parser.parse_args()

    # Отладочный вывод параметров (требование этапа 2)
    print("--- Загруженные параметры ---")
    print(f"VFS Path: {args.vfs_path}")
    print(f"Script:   {args.script}")
    print("-----------------------------")

    # Загружаем VFS в память
    if args.vfs_path:
        root_vfs = load_vfs(args.vfs_path)
    else:
        # Если путь не указан — создаем пустую VFS в памяти.
        root_vfs = {"type": "dir", "name": "vfs", "children": {}}

    # Создаем состояние
    state = ShellState(root_vfs)

    # Выполняем скрипт, если он передан.
    if args.script:
        run_script(state, args.script)

    # Запускаем интерактивный цикл
    repl(state)


if __name__ == "__main__":
    main()