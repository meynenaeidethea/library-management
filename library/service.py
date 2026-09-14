from datetime import date, timedelta

from .exceptions import (
    ActiveLoanNotFoundError,
    BookHasActiveLoansError,
    BookUnavailableError,
    BorrowingLimitError,
    DuplicateEntityError,
    EntityNotFoundError,
    InvalidReturnDateError,
)
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

    def borrow_book(self, isbn: str, user_id: int, borrowed_on: date) -> Loan:
        if isbn not in self.books:
            raise EntityNotFoundError(f"Book with ISBN {isbn} not exists!")
        elif user_id not in self.users:
            raise EntityNotFoundError(f"User with ID {user_id} not exists!")
        count_loans = 0
        count_books = 0
        for loan in self.loans:
            if loan.user_id == user_id and loan.returned_on is None:
                count_loans += 1
            if loan.isbn == isbn and loan.returned_on is None:
                count_books += 1
        if count_loans >= self.users[user_id].books_limit:
            raise BorrowingLimitError(
                f"Exceeds the limit of books [{count_loans}/{self.users[user_id].books_limit}]"
            )
        elif count_books >= self.books[isbn].total_copies:
            raise BookUnavailableError(f"These books (ISBN: {isbn}) are out of stock")
        loan = Loan(
            isbn=isbn,
            user_id=user_id,
            borrowed_on=borrowed_on,
            due_on=borrowed_on + timedelta(days=self.users[user_id].days_limit),
        )
        self.loans.append(loan)
        return loan

    def return_book(self, isbn: str, user_id: int, returned_on: date) -> Loan:
        if isbn not in self.books:
            raise EntityNotFoundError(f"Book with ISBN {isbn} not exists!")
        elif user_id not in self.users:
            raise EntityNotFoundError(f"User with ID {user_id} not exists!")
        for loan in self.loans:
            if (
                loan.isbn == isbn
                and loan.user_id == user_id
                and loan.returned_on is None
            ):
                if returned_on < loan.borrowed_on:
                    raise InvalidReturnDateError(
                        "Return date cannot be earlier than borrow date"
                    )
                loan.returned_on = returned_on
                return loan
        raise ActiveLoanNotFoundError("Loan not found!")

    def get_overdue_loans(self, on_date: date) -> list[Loan]:
        return [
            loan
            for loan in self.loans
            if loan.returned_on is None and loan.due_on < on_date
        ]

    def get_book_by_isbn(self, isbn: str) -> Book:
        if isbn not in self.books:
            raise EntityNotFoundError(f"Book with ISBN {isbn} does not exist")
        return self.books[isbn]

    def search_books_by_title(self, query: str) -> list[Book]:
        normalized_query = query.lower()
        return [
            book
            for book in self.books.values()
            if normalized_query in book.title.lower()
        ]

    def search_books_by_author(self, query: str) -> list[Book]:
        normalized_query = query.lower()
        return [
            book
            for book in self.books.values()
            if normalized_query in book.author.full_name.lower()
        ]

    def remove_book(self, isbn: str) -> None:
        if isbn not in self.books:
            raise EntityNotFoundError(f"Book with ISBN {isbn} does not exist")

        has_active_loans = any(
            loan.isbn == isbn and loan.returned_on is None for loan in self.loans
        )
        if has_active_loans:
            raise BookHasActiveLoansError(
                f"Cannot remove book with ISBN {isbn}: it has active loans"
            )

        del self.books[isbn]
