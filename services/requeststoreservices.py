import logging
import uuid

from sqlalchemy.orm import Session

from db.connection import db
from db.repositories.outreachrequestrespository import OutreachRequests
from schemas.inputstate import InputState

logger = logging.getLogger(__name__)


class OutreachRequestStore:
    def __init__(self) -> None:
        self.request_repository = OutreachRequests()

    def storeuserrequest(
        self,
        request: InputState,
        id: uuid.UUID,
        status: str,
    ) -> None:
        if not request:
            raise ValueError("request is required")
        if not id:
            raise ValueError("request id is required")
        if not status:
            raise ValueError("request status is required")

        try:
            with db.session_scope() as session:
                self.request_repository.store_requests(
                    request=request,
                    id=id,
                    status=status,
                    session=session,
                )
        except Exception:
            logger.exception("Error while storing outreach request")
            raise

    def update_status(
        self,
        id: uuid.UUID,
        status: str,
        session: Session,
    ) -> None:
        if not id:
            raise ValueError("request id is required")
        if not status:
            raise ValueError("request status is required")

        self.request_repository.update_status(
            id=id,
            status=status,
            session=session,
        )

    def get_prev_requests(
        self,
        session: Session,
    ) -> list[dict[str, str | int | None]]:
        results = self.request_repository.get_requests(session=session)
        return [
            {
                "id": str(request.id),
                "business1": request.business1,
                "business2": request.business2,
                "business3": request.business3,
                "location": request.location,
                "pitch": request.pitch,
                "search_place_count": request.search_place_count,
                "created_date": request.created_date.isoformat(),
                "request_status": request.request_status,
            }
            for request in results
        ]