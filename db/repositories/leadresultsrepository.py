import logging
import uuid
from decimal import Decimal

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from db.models.leadsresults import ClClientResult
from schemas.inputstate import Lead

logger = logging.getLogger(__name__)


class LeadsResults:
    def store_results(
        self,
        leads: list[Lead],
        request_id: uuid.UUID,
        session: Session,
    ) -> int:
        if not leads:
            return 0

        records = []
        for lead in leads:
            name = lead.get("name")
            if not name:
                raise ValueError("Each lead must include a business name")

            records.append({
                "id": request_id,
                "name": name,
                "category": lead.get("category"),
                "address": lead.get("address"),
                "phone": lead.get("phone"),
                "rating": (
                    Decimal(str(lead["rating"]))
                    if lead.get("rating") not in (None, "")
                    else None
                ),
                "google_map_url": lead.get("google_maps_url"),
                "cold_message": lead.get("cold_message"),
            })

        try:
            session.execute(insert(ClClientResult), records)
        except Exception:
            logger.exception("Error while storing lead results")
            raise

        logger.info("Lead results inserted count=%s", len(records))
        return len(records)

    def get_results(
        self,
        id: uuid.UUID,
        session: Session,
    ) -> list[ClClientResult]:
        try:
            statement = select(ClClientResult).where(
                ClClientResult.id == id,
            )
            return list(session.scalars(statement).all())
        except Exception:
            logger.exception("Error while fetching lead results")
            raise
