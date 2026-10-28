import logging
import uuid

from sqlalchemy import insert, update, select
from sqlalchemy.orm import Session

from db.models.outreachrequestmodel import ClOutreachRequest
from schemas.inputstate import InputState

logger = logging.getLogger(__name__)


class OutreachRequests:
    def store_requests(
        self,
        request: InputState,
        id: uuid.UUID,
        status: str,
        session: Session,
    ) -> None:
        record = {
            "id": id,
            "business1": request.get("business1"),
            "business2": request.get("business2"),
            "business3": request.get("business3"),
            "location": request.get("location"),
            "pitch": request.get("pitch"),
            "search_place_count": request.get("places_to_scrape", 1),
            "request_status": status,
        }

        try:
            session.execute(insert(ClOutreachRequest), [record])
        except Exception:
            logger.exception("Error while storing outreach request")
            raise

    def update_status(
        self,
        id: uuid.UUID,
        status: str,
        session: Session,
    ) -> None:
        try:
            result = session.execute(
                update(ClOutreachRequest)
                .where(ClOutreachRequest.id == id)
                .values(request_status=status)
            )
            if result.rowcount != 1:
                raise LookupError(f"Outreach request {id} was not found")
        except Exception:
            logger.exception("Error while updating outreach request status")
            raise

    def get_requests(self, session: Session):
        try:
            stmt = (
                select(ClOutreachRequest)
                .where(ClOutreachRequest.request_status == "success")
                .order_by(ClOutreachRequest.created_date.desc())
            )

            results = list(session.scalars(stmt).all())
            logger.info("Fetched previous outreach requests count=%s", len(results))
            return results
        except Exception:
            logger.exception("Error while fetching previous outreach requests")
            raise