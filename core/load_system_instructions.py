from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


class SystemInstructions:
    def __init__(self):
        self.system_instructions = (
            PROMPTS_DIR / "ai_system_instructions.txt"
        ).read_text(encoding="utf-8")
        self.message_prompt = (
            PROMPTS_DIR / "coldmessageinstructions.txt"
        ).read_text(encoding="utf-8")


prompts = SystemInstructions()
