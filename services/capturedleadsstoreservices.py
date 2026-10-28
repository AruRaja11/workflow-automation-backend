import logging
import uuid

from sqlalchemy.orm import Session

from db.connection import db
from db.models.leadsresults import ClClientResult
from db.repositories.leadresultsrepository import LeadsResults
from schemas.inputstate import Lead

logger = logging.getLogger(__name__)


class LeadResultServices:
    def __init__(self) -> None:
        self.lead_repository = LeadsResults()

    def store_retrieved_leads(
        self,
        leads: list[Lead],
        request_id: uuid.UUID,
        session: Session,
    ) -> int:
        try:
            return self.lead_repository.store_results(
                leads=leads,
                request_id=request_id,
                session=session,
            )
        except Exception:
            logger.exception("Error while storing fetched lead results")
            raise

    def get_fetched_leads(self, id: uuid.UUID) -> list[ClClientResult]:
        try:
            with db.session_scope() as session:
                leads = self.lead_repository.get_results(id, session)

            logger.info("Lead results fetched count=%s", len(leads))
            return leads
        except Exception:
            logger.exception("Error while fetching stored lead results")
            raise
