import logging
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import wraps
from typing import Concatenate, ParamSpec, Protocol, TypeVar

from app.domain.articles.commands import get_articles_command
from app.domain.context import ContextProtocol

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


class UnitOfWorkProtocol(Protocol):
    @contextmanager
    def transaction(self) -> Iterator[None]: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class TransactionalContextProtocol(UnitOfWorkProtocol, ContextProtocol): ...


class Domain:
    def command_handler(
        self, func: Callable[Concatenate[TransactionalContextProtocol, P], R]
    ) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start_time = time.perf_counter()
            with self.context.transaction():
                try:
                    result = func(self.context, *args, **kwargs)
                # Catch all exceptions to ensure rollback
                except Exception as error:
                    self.context.rollback()
                    logger.debug(
                        f"Command '{func.__name__}' failed with "
                        f"{error.__class__.__name__}: {error}"
                    )
                    raise

                self.context.commit()
                duration = time.perf_counter() - start_time
                logger.debug(
                    f"Command '{func.__name__}' succeeded in {duration * 1000:.1f} ms",
                )
                return result

        return wrapper

    def __init__(self, context: TransactionalContextProtocol):
        self.context = context

        self.get_articles = self.command_handler(get_articles_command)
