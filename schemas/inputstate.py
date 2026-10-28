from typing import Annotated, NotRequired, TypedDict

from langgraph.graph import MessagesState
from pydantic import Field


class InputState(TypedDict):
    business1: str
    business2: str
    business3: str
    location: str
    pitch: str
    places_to_scrape: NotRequired[Annotated[int, Field(ge=1, le=100)]]


class Lead(TypedDict, total=False):
    name: str | None
    category: str | None
    address: str | None
    phone: str | None
    website: str | None
    rating: float | None
    reviews_count: int | None
    google_maps_url: str | None
    cold_message: str | None


class GoogleMapScrapper(TypedDict):
    leads: list[Lead]
    leads_count: int


class OverallState(MessagesState, total=False):
    scrapinginputs: InputState
    scrap_leads: GoogleMapScrapper
    output_path: str
