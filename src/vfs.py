###Модуль виртуальной файловой системы (VFS).
import os


def load_vfs(real_path: str) -> dict:
    """
    Загружает структуру реальной директории в память.
    Возвращает корневой узел в виде вложенного словаря.
    Диск не модифицируется.
    """
    if not os.path.isdir(real_path):
        print(f"Ошибка: VFS директория не найдена: {real_path}")
        return {}

    root_node = {"type": "dir", "name": os.path.basename(real_path), "children": {}}

    for dirpath, dirnames, filenames in os.walk(real_path):
        rel_path = os.path.relpath(dirpath, real_path)
        current_node = root_node
        
        if rel_path != ".":
            for part in rel_path.split(os.sep):
                current_node = current_node["children"][part]

        for d in dirnames:
            current_node["children"][d] = {"type": "dir", "name": d, "children": {}}

        for f in filenames:
            file_path = os.path.join(dirpath, f)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
            except (UnicodeDecodeError, OSError):
                content = "[binary file]"
                
            current_node["children"][f] = {
                "type": "file", 
                "name": f, 
                "content": content
            }

    return root_node