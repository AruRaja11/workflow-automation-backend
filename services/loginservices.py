import logging

from db.connection import db
from db.repositories.usercredrepository import UserRepository

logger = logging.getLogger(__name__)


class LoginServices:
    def verify_login(self, username: str, password: str) -> int:
        with db.session_scope() as session:
            true_password = UserRepository(session).get_user(username=username)

        if true_password is None:
            return 0

        return int(true_password == password)
