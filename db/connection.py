from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from core.config import setting


class DBInit:
    def __init__(self) -> None:
        database_url = setting.db_url.strip().strip('"').strip("'")
        if not database_url:
            raise ValueError("Invalid Database Url")

        if database_url.startswith("postgres://"):
            database_url = "postgresql+psycopg2://" + database_url.removeprefix(
                "postgres://"
            )
        elif database_url.startswith("postgresql://"):
            database_url = "postgresql+psycopg2://" + database_url.removeprefix(
                "postgresql://"
            )

        parsed_url = make_url(database_url)
        connect_args = {}
        if parsed_url.host and (
            parsed_url.host.endswith(".supabase.co")
            or parsed_url.host.endswith(".pooler.supabase.com")
        ) and "sslmode" not in parsed_url.query:
            connect_args["sslmode"] = "require"

        self.engine = create_engine(
            url=parsed_url,
            echo=False,
            pool_pre_ping=True,
            connect_args=connect_args,
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
