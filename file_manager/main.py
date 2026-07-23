import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="File manager utility")
    parser.add_argument("--dir", required=True, help="Directory path")
    parser.add_argument("--ext", required=True, help="File extension (e.g. .txt)")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompts")
    parser.add_argument(
        "--action",
        choices=["count", "delete", "move"],
        default="count",
        help="Action to perform",
    )
    return parser.parse_args()


def count_files(directory: Path, extension: str) -> int:
    """Count files with given extension in directory"""

    total_files = 0

    if not extension.startswith("."):
        extension = f".{extension}"

    for item in directory.iterdir():
        if item.is_file() and item.suffix.lower() == extension.lower():
            total_files += 1

    return total_files


def delete_files(directory: Path, extension: str, yes: bool = False) -> int:

    if not extension.startswith("."):
        extension = f".{extension}"

    total_files = count_files(directory, extension)
    if total_files == 0:
        print("Файлов для удаления не найдено.")
        return 0

    if not yes:
        answer = input(f"Удалить {total_files} файлов? [y/n]: ")
        if answer.lower() not in ["y", "yes"]:
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
                print(f"Нет прав на удаление: {item.name}")
            except Exception as e:
                print(f"Ошибка при удалении {item.name}: {e}")

    return deleted_count


def move_files(
    directory: Path, extension: str, target_dir: Path, yes: bool = False
) -> int:
    if not extension.startswith("."):
        extension = f".{extension}"

    total_files = count_files(directory, extension)

    if total_files == 0:
        print(f"Файлов с расширением {extension} не найдено")
        return 0
    # проверка существования директории, в которую будут перемещены файлы
    if not Path(target_dir).exists():
        # Если такой директории нет то создать, parent=True - создать родительские папки, exist_ok=True - если папка уже есть ничего не создавать
        target_dir.mkdir(parents=True, exist_ok=True)
    total_files_moved = 0
    # Спрашиваем пользователя хочет ли он переместить файлы если нет то выходим и возвращаем ноль перемещенных файлов
    answer = input("Вы хотите переместить файлы с выбранным расширением (y/n): ")
    if answer == "n":
        return total_files_moved
    # Перемещаем файлы и увеличиваем счетчик
    for item in directory.iterdir():
        # Проверка действительности файла и его расширения
        if item.is_file() and item.suffix.lower() == extension:
            # Создание пути для перемещения
            target_path = target_dir / item.name
            # Проверка на существование файла, если существует, по пропускаем
            if target_path.exists():
                print(f"Файл уже существует: {target_path.name}")
                continue
            # Переносим файл
            item.rename(target_path)
            total_files_moved += 1
    # Возврат количества перемещенных файлов
    return total_files_moved


def main():
    args = parse_args()
    directory = Path(args.dir)
    extension = args.ext

    print(f"Directory: {directory}")
    print(f"Extension: {extension}")
    print(f"Action: {args.action}")

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
    elif args.action == "move":
        target_dir = args.target
        if not target_dir:
            pass
        total_files_moved = move_files(
            directory,
            extension,
        )
    else:
        print(f"Действие '{args.action}' пока не реализовано. Скоро будет!")


if __name__ == "__main__":
    main()
