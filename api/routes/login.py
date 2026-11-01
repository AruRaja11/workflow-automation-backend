from fastapi import APIRouter
from services.loginservices import LoginServices

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

service = LoginServices()


@router.get("/login")
async def user_login(username: str, password: str):
    try:
        return service.verify_login(username=username, password=password)
    except Exception as e:
        raise e
