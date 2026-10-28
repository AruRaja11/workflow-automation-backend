from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import setting


class DBInit:
    def __init__(self) -> None:
        database_url = setting.db_url
        if not database_url:
            raise ValueError("Invalid Database Url")

        self.engine = create_engine(
            url=database_url,
            echo=False,
            pool_pre_ping=True,
        )
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        with self.session_factory.begin() as session:
            yield session


db = DBInit()
