class LibraryError(Exception):
    pass


class DuplicateEntityError(LibraryError):
    pass


class EntityNotFoundError(LibraryError):
    pass


class BorrowingLimitError(LibraryError):
    pass


class BookUnavailableError(LibraryError):
    pass


class ActiveLoanNotFoundError(LibraryError):
    pass


class InvalidReturnDateError(LibraryError):
    pass


class BookHasActiveLoansError(LibraryError):
    pass
