import logging

from langgraph.graph import StateGraph, START
from core.logging_cofig import setup_logging

from nodes.aicoldmessage import writecoldmessage
from nodes.gm_scraper import google_map_scrapper
from nodes.saveleads import storeleads
from schemas.inputstate import OverallState

setup_logging()

logger = logging.getLogger(__name__)


class ClientAcquitionGraph:
    def __init__(self):
        self.builder = StateGraph(OverallState)

    def add_node(self):

        # register all the nodes 

        self.builder.add_node(
            "google_map_scrapper",
            google_map_scrapper
        )

        self.builder.add_node(
            "writecoldmessage",
            writecoldmessage
        )
        self.builder.add_node(
            "storeleads",
            storeleads
        ) 


    def add_edges(self):
        self.builder.add_edge(START, "google_map_scrapper")
        self.builder.add_edge("google_map_scrapper", "writecoldmessage")
        self.builder.add_edge("writecoldmessage", "storeleads")

    def build(self):
        logger.info("Compiling outreach graph")
        self.add_node()
        self.add_edges()
        compiled_graph = self.builder.compile()
        logger.info("Outreach graph compiled successfully")
        return compiled_graph


graph = ClientAcquitionGraph().build()