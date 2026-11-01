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
        result = service.verify_login(username=username, password=password)

        if result == 0:
            return {
                "status": "failed",
                "response": "invalid username or password"
            }

        if result == 1:
            return {
                "status": "success",
                "response": "successfully logged in"
            }
    except Exception as e:
        return {
            "status": "failed",
            "response": f"exception: {e}"
        }
