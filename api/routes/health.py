from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

@router.get("/")
async def health_check():
    return {
        "status": "success",
        "message": "successfully connected"
    }