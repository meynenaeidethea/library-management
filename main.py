from library.cli import run_cli
from library.service import LibraryService


def main() -> None:
    service = LibraryService()
    run_cli(service)


if __name__ == "__main__":
    main()
