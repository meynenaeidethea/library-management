class LibraryError(Exception):
    pass


class DuplicateEntityError(LibraryError):
    pass


class EntityNotFoundError(LibraryError):
    pass
