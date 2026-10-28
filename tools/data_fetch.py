from langchain_core.tools import tool
from core.config import openai
from schemas.inputstate import InputState

@tool
def scrap_business(state:InputState):
    try:    
        business1 = state.get("business1")
        business2 = state.get("business2")
        business3 = state.get("business3")

        location = state.get("location")
        pitch = state.get("pitch")

        if any([business1, business2, business3, location, pitch]) == None or location == "":
            raise ValueError("static inputs cannot be empty")

        

    except Exception as e:
        raise e