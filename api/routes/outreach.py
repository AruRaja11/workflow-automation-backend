import logging

from fastapi import APIRouter, HTTPException
from schemas.inputstate import InputState, OverallState

from services.outreachservicelayer import outreachservices

logger = logging.getLogger(__name__)


# router workflow

router = APIRouter(
    prefix="/outreach",
    tags=["Outreach"],
)

outreach = outreachservices()

@router.post(
    "/generate",
    response_model=OverallState
)
async def generate_outreach(request:InputState):
    try:
        return await outreach.generate(request)
        
    except Exception as e:
        logger.error(
            "Outreach endpoint failed exception_type=%s",
            type(e).__name__,
        )
        raise HTTPException(
            status_code=500,
            detail=f"outreach failed: {e}"
        )