import logging

from core.config import setting
from core.load_system_instructions import prompts
from openai import OpenAI
from schemas.inputstate import OverallState

logger = logging.getLogger(__name__)


def writecoldmessage(state: OverallState) -> dict:
    logger.info("Cold-message generation started")
    api_key = setting.openai_key
    if not api_key:
        logger.error("Cold-message generation cannot start: OpenAI key is not configured")
        raise ValueError("OPENAI_API_KEY is missing")

    scraped_data = state.get("scrap_leads")
    if not scraped_data or "leads" not in scraped_data:
        logger.warning("Cold-message generation stopped: scraped leads are missing")
        raise ValueError(
            "No scraped leads found in graph state. Run the graph from its "
            "start so google_map_scrapper populates 'scrap_leads' before "
            "writecoldmessage runs."
        )

    leads = scraped_data["leads"]
    logger.info("Cold-message generation processing lead_count=%s", len(leads))
    client = OpenAI(api_key=api_key)

    generated_count = 0
    skipped_count = 0
    for index, lead in enumerate(leads, start=1):
        if not lead.get("phone"):
            lead["cold_message"] = ""
            skipped_count += 1
            logger.info("Cold-message skipped lead_index=%s reason=missing_phone", index)
            continue

        try:
            temp_prompt = prompts.message_prompt.format(
                name=lead.get("name") or "there",
                category=lead.get("category") or "business",
                address=lead.get("address") or "",
                rating=lead.get("rating") or "not available",
            )
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": prompts.system_instructions},
                    {"role": "user", "content": temp_prompt},
                ],
            )
        except Exception as exc:
            logger.error(
                "Cold-message generation failed lead_index=%s exception_type=%s",
                index,
                type(exc).__name__,
            )
            raise

        lead["cold_message"] = response.choices[0].message.content or ""
        generated_count += 1

    logger.info(
        "Cold-message generation completed generated_count=%s skipped_count=%s",
        generated_count,
        skipped_count,
    )
    return {
        "scrap_leads": {
            "leads": leads,
            "leads_count": len(leads),
        }
    }
