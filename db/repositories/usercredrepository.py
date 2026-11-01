from sqlalchemy import select
from db.models.users import Users
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, username: str) -> str | None:
        stmt = select(Users.password).where(Users.username == username)
        return self.session.scalar(stmt)
