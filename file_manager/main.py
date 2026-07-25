import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="File manager utility")
    parser.add_argument("--dir", required=True, help="Directory path")
    parser.add_argument("--ext", required=True, help="File extension (e.g. .txt)")
    parser.add_argument("--target", help="Target directory for the move action")
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
    # target_dir - не нужно передавать в экземпляр класса Path, так как он уже является экземпляром этого класса
    if not target_dir.exists():
        # Если такой директории нет то создать, parents=True - создать родительские папки, exist_ok=True - если папка уже есть ничего не создавать
        target_dir.mkdir(parents=True, exist_ok=True)
    total_files_moved = 0
    # Проверить параметр на согласие перемещения файлов, если не было согласия получено из консоли
    if not yes:
        answer = input("Вы хотите переместить файл(ы) с выбранным расширением (y/n): ")
        # Проверяем только положительный ответ, все остальные будут считаться отрицательными
        if answer.lower() not in ["yes", "y"]:
            print("Отменено пользователем")
            return total_files_moved
    # Перемещаем файлы и увеличиваем счетчик
    for item in directory.iterdir():
        # Проверка действительности файла и его расширения
        if item.is_file() and item.suffix.lower() == extension.lower():
            # Создание пути для перемещения
            target_path = target_dir / item.name
            # Проверка на существование файла, если существует, по пропускаем
            if target_path.exists():
                print(f"Файл уже существует: {target_path.name}")
                continue
            # Переносим файл
            # обработка ошибок 1 - если не достаточно прав, 2 - ошибка при перемещении
            try:
                item.rename(target_path)
                print(f"Файл {item.name} перемещен -> {target_path}")
                total_files_moved += 1
            except PermissionError:
                print(f"Нет прав на перемещение {item.name}")
            except Exception:
                print(f"Возникла ошибка при перемещении {item.name}")
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
        # Проверка что в консоли передан параметр --target
        if not args.target:
            print("Ошибка: для действия 'move' нужно указать '--target'")
            return
        # Создание экземпляра объекта Path
        target_dir = Path(args.target)
        # Перемещение файлов и их подсчет
        total_files_moved = move_files(directory, extension, target_dir, args.yes)
        print(f"Перемещено - {total_files_moved} файл(ов)")
    else:
        print(f"Действие '{args.action}' пока не реализовано. Скоро будет!")


if __name__ == "__main__":
    main()
