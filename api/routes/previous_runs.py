import logging
import uuid

from fastapi import APIRouter, HTTPException
from services.outreachservicelayer import outreachservices

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/runs",
    tags=["Runs"],
)


requests = outreachservices()


@router.get("")
async def previous_runs():
    try:
        return requests.previous_runs()

    except Exception as exc:
        logger.exception("Error in previous runs route")
        raise HTTPException(
            status_code=500,
            detail="Could not load previous outreach runs.",
        ) from exc


@router.get("/{run_id}/executions")
async def run_executions(run_id: uuid.UUID):
    try:
        leads = requests.leadresultservices.get_fetched_leads(run_id)
        return [
            {
                "seq_id": lead.seq_id,
                "name": lead.name,
                "category": lead.category,
                "address": lead.address,
                "phone": lead.phone,
                "rating": lead.rating,
                "google_map_url": lead.google_map_url,
                "cold_message": lead.cold_message,
                "created_date": lead.created_date,
                "is_active": lead.is_active,
            }
            for lead in leads
        ]
    except Exception as exc:
        logger.exception("Error loading outreach executions run_id=%s", run_id)
        raise HTTPException(
            status_code=500,
            detail="Could not load this run's execution results.",
        ) from exc