### Модуль реализации команд эмулятора ###
import calendar
import datetime


class ShellState:
    # Хранит состояние оболочки (текущая папка и история)

    def __init__(self, root_vfs: dict) -> None:
        # Инициализирует состояние корневой директорией
        self.root = root_vfs
        self.current_dir = root_vfs
        self.history: list[str] = []


def cmd_ls(state: ShellState, args: list[str]) -> None:
    # Выводит содержимое текущей директории
    children = state.current_dir.get("children", {})
    if not children:
        return
    for name, node in children.items():
        suffix = "/" if node["type"] == "dir" else ""
        print(f"{name}{suffix}")


def cmd_cd(state: ShellState, args: list[str]) -> None:
    # Меняет текущую директорию
    if not args:
        return
        
    target = args[0]
    
    # Обработка перехода в корень
    if target == "/":
        state.current_dir = state.root
        return
        
    children = state.current_dir.get("children", {})
    if target not in children:
        print(f"cd: {target}: директория не найдена")
        return
        
    node = children[target]
    if node["type"] != "dir":
        print(f"cd: {target}: не является директорией")
        return
        
    state.current_dir = node


def cmd_history(state: ShellState, args: list[str]) -> None:
    # Выводит историю выполненных команд
    for i, cmd in enumerate(state.history, 1):
        print(f"{i:3}  {cmd}")


def cmd_cal(state: ShellState, args: list[str]) -> None:
    # Выводит календарь на текущий месяц
    now = datetime.datetime.now()
    print(calendar.month(now.year, now.month))


def cmd_mv(state: ShellState, args: list[str]) -> None:
    # Перемещает или переименовывает файл/папку в памяти VFS
    if len(args) != 2:
        print("mv: требуется 2 аргумента (источник и назначение)")
        return
    
    src, dst = args
    children = state.current_dir.get("children", {})
    
    if src not in children:
        print(f"mv: '{src}' не найден")
        return
        
    if dst in children:
        print(f"mv: '{dst}' уже существует")
        return
        
    node = children.pop(src)
    """
     Если новое имя содержит слэш (например, docs/file.txt), 
     нужно нырнуть в папку docs и положить туда.
    """
    if "/" in dst:
        parts = dst.split("/")
        target_dir_name = parts[0]
        new_name = parts[-1]
        
        if target_dir_name not in children or children[target_dir_name]["type"] != "dir":
            print(f"mv: '{target_dir_name}' не является директорией")
            children[src] = node # Возвращаем файл на место
            return
            
        children[target_dir_name]["children"][new_name] = node
    else:
        # Просто переименование
        children[dst] = node
        
    print(f"Перемещено: {src} -> {dst}")