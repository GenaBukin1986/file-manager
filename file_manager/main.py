import argparse
from pathlib import Path

def parse_args():
    parse = argparse.ArgumentParser(description="File manager utility")
    parse.add_argument("--dir", required=True, help="Directory path")
    parse.add_argument("--ext", required=True, help="File extension (e.g.m .txt)")
    parse.add_argument("--yes", action="store_true", help="Skip confirmation prompts")
    parse.add_argument(
        "--action", 
        choices=["count", "delete", "move"],
        default="count",
        help="Action to perform"
        )
    return parse.parse_args()

def count_files(directory: Path, extension: str) -> int:
    """Count files with given extension in directory"""
    # TODO: Реализовать подсчет
    total_files = 0

    if not extension.startswith("."):
        extension = f'.{extension}'

    for item in directory.iterdir():
        if item.is_file() and item.suffix.lower() == extension.lower():
            total_files += 1

    return total_files

def delete_files(directory: Path, extension: str, yes: bool = False) -> int:
    
    if not extension.startswith("."):
        extension = f'.{extension}'

    total_files = count_files(directory, extension)
    if total_files == 0:
        print("Файлов для удаления не найдено.")
        return 0
    
    if not yes:
        answer = input(f"Удалить {total_files} файлов? [y/n]: ")
        if answer.lower() not in ['y', 'yes']:
            print("Отменено пользователем.")
            return 0

    deleted_count = 0

    for item in directory.iterdir():
        if item.is_file() and item.suffix.lower() == extension.lower():
            try:
                print(f"Удаляем файл: {item.name}")
                item.unlink()
                deleted_count += 1
            except PermissionError:
                print(f'Нет прав на удаление: {item.name}')
            except Exception as e:
                print(f'Ошибка при удалении {item.name}: {e}')

    return total_files

def main():
    args = parse_args()
    directory = Path(args.dir)
    extension = args.ext

    print(f'Directory: {directory}')
    print(f'Extension: {extension}')
    print(f'Action: {args.action}')

    if not directory.exists():
        print(f"Ошибка: Директория '{directory}' не существует")
        return
    
    if not directory.is_dir():
        print(f"Ошибка: '{directory}' не является директорией.")
        return
    
    if args.action == "count":
        total = count_files(directory, extension)
        print(f"Найдено файлов: {total}")

    elif args.action == "delete":
        total = delete_files(directory, extension, args.yes)
        print(f"Удалено файлов: {total}")
    else:
        print(f"Действие '{args.action}' пока не реализовано. Скоро будет!")
    # TODO: Вызвать нужную функцию в зависимости от action


if __name__ == "__main__":
    main()
