from .exceptions import DuplicateEntityError
from .models import Author, Book, Loan, User


class LibraryService:
    def __init__(self) -> None:
        self.books: dict[str, Book] = {}
        self.authors: dict[int, Author] = {}
        self.users: dict[int, User] = {}
        self.loans: list[Loan] = []

    def add_author(self, author: Author) -> None:
        if author.author_id in self.authors:
            raise DuplicateEntityError(
                f"Author with ID {author.author_id} already exists"
            )
        self.authors[author.author_id] = author

    def add_book(self, book: Book) -> None:
        if book.author.author_id not in self.authors:
            self.authors[book.author.author_id] = book.author
        elif self.authors[book.author.author_id].full_name != book.author.full_name:
            raise DuplicateEntityError(
                f"Author with this ID {book.author.author_id} already exists!"
            )
        if book.isbn in self.books:
            raise DuplicateEntityError(f"Book with ISBN {book.isbn} already exists!")
        self.books[book.isbn] = book

    def add_user(self, user: User) -> None:
        if user.user_id in self.users:
            raise DuplicateEntityError(f"User with ID {user.user_id} already exists!")
        self.users[user.user_id] = user
