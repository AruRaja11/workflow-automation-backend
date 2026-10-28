import logging
import uuid
from time import perf_counter

from db.connection import db
from graph.maingraph import graph
from schemas.inputstate import InputState, OverallState
from services.capturedleadsstoreservices import LeadResultServices
from services.requeststoreservices import OutreachRequestStore

logger = logging.getLogger(__name__)


class outreachservices:
    def __init__(self) -> None:
        self.graph = graph
        self.leadresultservices = LeadResultServices()
        self.outreachrequestservices = OutreachRequestStore()

    async def generate(self, request: InputState) -> OverallState:
        started_at = perf_counter()
        request_id = uuid.uuid4()
        request_stored = False
        logger.info("Outreach workflow started")

        try:
            self.outreachrequestservices.storeuserrequest(
                request=request,
                id=request_id,
                status="pending",
            )
            request_stored = True

            result = await self.graph.ainvoke({
                "messages": [],
                "scrapinginputs": request,
            })
            leads = result.get("scrap_leads", {}).get("leads", [])

            with db.session_scope() as session:
                self.leadresultservices.store_retrieved_leads(
                    leads=leads,
                    request_id=request_id,
                    session=session,
                )
                self.outreachrequestservices.update_status(
                    id=request_id,
                    status="success",
                    session=session,
                )
        except Exception as exc:
            if request_stored:
                try:
                    with db.session_scope() as session:
                        self.outreachrequestservices.update_status(
                            id=request_id,
                            status="failed",
                            session=session,
                        )
                except Exception:
                    logger.exception(
                        "Could not mark outreach request as failed request_id=%s",
                        request_id,
                    )

            logger.error(
                "Outreach workflow failed request_id=%s exception_type=%s duration_ms=%.2f",
                request_id,
                type(exc).__name__,
                (perf_counter() - started_at) * 1000,
            )
            raise

        lead_count = result.get("scrap_leads", {}).get("leads_count", len(leads))
        logger.info(
            "Outreach workflow completed request_id=%s lead_count=%s duration_ms=%.2f",
            request_id,
            lead_count,
            (perf_counter() - started_at) * 1000,
        )
        return result

    def previous_runs(self):
        try:
            with db.session_scope() as session:
                results = self.outreachrequestservices.get_prev_requests(session)

            return results
        except Exception:
            logger.exception("Error while loading previous outreach runs")
            raise