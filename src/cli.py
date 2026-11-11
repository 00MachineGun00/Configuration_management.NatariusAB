### Модуль для работы с аргументами командной строки ###
import argparse


def build_parser() -> argparse.ArgumentParser:
    # Создает и возвращает парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Эмулятор Shell (Вариант 15)")
    parser.add_argument("--vfs-path", help="Путь к директории VFS на диске")
    parser.add_argument("--script", help="Путь к стартовому скрипту")
    return parser