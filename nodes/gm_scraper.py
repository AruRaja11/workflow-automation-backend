
import logging

import requests

from core.config import setting
from schemas.inputstate import OverallState
from schemas.inputstate import Lead

logger = logging.getLogger(__name__)


def google_map_scrapper(state: OverallState) -> dict:
    logger.info("Google Maps scraper started")
    api_key = setting.apify_key
    if not api_key:
        logger.error("Google Maps scraper cannot start: Apify token is not configured")
        raise ValueError("APIFY_API_TOKEN is missing from .env")

    actor_input = {
        "enableCompetitorAnalysis": False,
        "includeWebResults": False,
        "language": "en",
        "locationQuery": state["scrapinginputs"]["location"],
        "maxCrawledPlacesPerSearch": state["scrapinginputs"].get("places_to_scrape", 1),
        "maximumLeadsEnrichmentRecords": 0,
        "scrapeContacts": False,
        "scrapeDirectories": False,
        "scrapeImageAuthors": False,
        "scrapeOrderOnline": False,
        "scrapePlaceDetailPage": False,
        "scrapeReviewsPersonalData": False,
        "scrapeSocialMediaProfiles": {
            "facebooks": False,
            "instagrams": False,
            "tiktoks": False,
            "twitters": False,
            "youtubes": False,
        },
        "scrapeTableReservationProvider": False,
        "searchStringsArray": [
            state["scrapinginputs"]["business1"],
            state["scrapinginputs"]["business2"],
            state["scrapinginputs"]["business3"],
        ],
        "skipClosedPlaces": True,
        "verifyLeadsEnrichmentEmails": False,
        "website": "withoutWebsite",
    }

    url = (
        "https://api.apify.com/v2/acts/"
        "compass~crawler-google-places/"
        "run-sync-get-dataset-items"
    )

    try:
        response = requests.post(
            url,
            params={"token": api_key},
            json=actor_input,
            timeout=180,
        )
        response.raise_for_status()
        businesses = response.json()

    except requests.RequestException as exc:
        logger.error(
            "Google Maps scraper request failed exception_type=%s",
            type(exc).__name__,
        )
        raise RuntimeError(
            f"Apify Google Maps scraping failed: {exc}"
        ) from exc

    leads: list[Lead] = []

    for business in businesses:
        leads.append({
            "name": business.get("title"),
            "category": business.get("categoryName"),
            "address": business.get("address"),
            "phone": business.get("phone"),
            "website": business.get("website"),
            "rating": business.get("totalScore"),
            "reviews_count": business.get("reviewsCount"),
            "google_maps_url": business.get("url"),
        })

    if leads:
        logger.info("Google Maps scraper completed lead_count=%s", len(leads))
    else:
        logger.warning("Google Maps scraper completed with no leads")

    return {
        "scrap_leads": {
            "leads": leads,
            "leads_count": len(leads),
        }
    }
