from datetime import date

from .exceptions import LibraryError
from .models import Author, Book, Faculty, Guest, Student, User
from .service import LibraryService


def run_cli(service: LibraryService) -> None:
    handlers = {
        "1": _add_author,
        "2": _add_book,
        "3": _add_user,
        "4": _borrow_book,
        "5": _return_book,
        "6": _search_by_isbn,
        "7": _search_by_title,
        "8": _search_by_author,
        "9": _show_overdue_loans,
        "10": _remove_book,
    }

    while True:
        _show_menu()
        try:
            command = input("Choose an action: ").strip()
        except EOFError:
            print("\nGoodbye!")
            return

        handler = handlers.get(command)
        if handler is None:
            print("Unknown command")
            continue

        try:
            handler(service)
        except LibraryError as error:
            print(f"Error: {error}")
        except ValueError:
            print("Invalid input. Enter numeric IDs and dates as YYYY-MM-DD")


def _show_menu() -> None:
    print(
        "\nLibrary management system\n"
        "1. Add author\n"
        "2. Add book\n"
        "3. Register user\n"
        "4. Borrow book\n"
        "5. Return book\n"
        "6. Find by ISBN\n"
        "7. Search by title\n"
        "8. Search by author\n"
        "9. Show overdue loans\n"
        "10. Remove book\n"
        "Ctrl+D to exit"
    )


def _add_author(service: LibraryService) -> None:
    author = Author(
        author_id=int(input("Author ID: ")),
        full_name=input("Author name: ").strip(),
    )
    service.add_author(author)
    print("Author added")


def _add_book(service: LibraryService) -> None:
    author = Author(
        author_id=int(input("Author ID: ")),
        full_name=input("Author name: ").strip(),
    )
    book = Book(
        isbn=input("ISBN: ").strip(),
        title=input("Title: ").strip(),
        total_copies=int(input("Total copies: ")),
        author=author,
    )
    service.add_book(book)
    print("Book added")


def _add_user(service: LibraryService) -> None:
    user_classes: dict[str, type[User]] = {
        "student": Student,
        "faculty": Faculty,
        "guest": Guest,
    }
    user_type = input("User type (student/faculty/guest): ").strip().lower()
    user_class = user_classes.get(user_type)
    if user_class is None:
        raise ValueError

    user = user_class(
        user_id=int(input("User ID: ")),
        name=input("User name: ").strip(),
    )
    service.add_user(user)
    print("User registered")


def _borrow_book(service: LibraryService) -> None:
    loan = service.borrow_book(
        isbn=input("ISBN: ").strip(),
        user_id=int(input("User ID: ")),
        borrowed_on=_read_date("Borrow date (YYYY-MM-DD): "),
    )
    print(f"Book borrowed. Due date: {loan.due_on.isoformat()}")


def _return_book(service: LibraryService) -> None:
    returned_on = _read_date("Return date (YYYY-MM-DD): ")
    service.return_book(
        isbn=input("ISBN: ").strip(),
        user_id=int(input("User ID: ")),
        returned_on=returned_on,
    )
    print(f"Book returned on {returned_on.isoformat()}.")


def _search_by_isbn(service: LibraryService) -> None:
    book = service.get_book_by_isbn(input("ISBN: ").strip())
    _print_book(book)


def _search_by_title(service: LibraryService) -> None:
    _print_books(service.search_books_by_title(input("Title query: ").strip()))


def _search_by_author(service: LibraryService) -> None:
    _print_books(service.search_books_by_author(input("Author query: ").strip()))


def _show_overdue_loans(service: LibraryService) -> None:
    on_date = _read_date("Check date (YYYY-MM-DD): ")
    loans = service.get_overdue_loans(on_date)
    if not loans:
        print("No overdue loans")
        return

    for loan in loans:
        print(
            f"ISBN: {loan.isbn}; user ID: {loan.user_id}; "
            f"due on: {loan.due_on.isoformat()}"
        )


def _remove_book(service: LibraryService) -> None:
    service.remove_book(input("ISBN: ").strip())
    print("Book removed")


def _read_date(prompt: str) -> date:
    return date.fromisoformat(input(prompt).strip())


def _print_books(books: list[Book]) -> None:
    if not books:
        print("No books found")
        return

    for book in books:
        _print_book(book)


def _print_book(book: Book) -> None:
    print(
        f"ISBN: {book.isbn}; title: {book.title}; "
        f"author: {book.author.full_name}; copies: {book.total_copies}"
    )
