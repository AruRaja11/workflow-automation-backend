import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

from schemas.inputstate import OverallState

logger = logging.getLogger(__name__)


def storeleads(state: OverallState) -> dict[str, str]:
    leads = state.get("scrap_leads", {}).get("leads", [])
    if not leads:
        logger.warning("Lead export skipped: no leads are available")
        raise ValueError("Cannot retrieve leads: the scraper returned no leads")

    logger.info("Lead export started lead_count=%s", len(leads))
    try:
        data = pd.DataFrame(
            [
                {
                    "name": lead.get("name"),
                    "category": lead.get("category"),
                    "address": lead.get("address"),
                    "phone": lead.get("phone"),
                    "rating": lead.get("rating"),
                    "google_map_url": lead.get("google_maps_url"),
                    "cold_message": lead.get("cold_message"),
                }
                for lead in leads
            ]
        )

        output_dir = Path("outcome")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"leads_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
        data.to_excel(output_path, index=False)
    except Exception as exc:
        logger.error(
            "Lead export failed lead_count=%s exception_type=%s",
            len(leads),
            type(exc).__name__,
        )
        raise

    logger.info(
        "Lead export completed lead_count=%s output_path=%s",
        len(leads),
        output_path,
    )
    return {"output_path": str(output_path)}
