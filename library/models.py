from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import ClassVar


@dataclass
class Author:
    author_id: int
    full_name: str


@dataclass
class Book:
    isbn: str
    title: str
    total_copies: int
    author: Author


@dataclass
class User(ABC):
    user_id: int
    name: str

    # правила займа: лимит книг и число дней
    @property
    @abstractmethod
    def books_limit(self) -> int:
        pass

    @property
    @abstractmethod
    def days_limit(self) -> int:
        pass


class Student(User):
    books_limit: ClassVar[int] = 3
    days_limit: ClassVar[int] = 14


class Faculty(User):
    books_limit: ClassVar[int] = 10
    days_limit: ClassVar[int] = 30


class Guest(User):
    books_limit: ClassVar[int] = 1
    days_limit: ClassVar[int] = 7


@dataclass
class Loan:
    isbn: str
    user_id: int
    borrowed_on: date
    due_on: date
    returned_on: date | None = None
