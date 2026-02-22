from dataclasses import dataclass
from .prompts import SYSTEM_PROMPT, instruction_prompt, few_shot_prompt


@dataclass
class LLMResult:
    reply: str
    model: str = "stub"
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class LLMService:
    def generate(self, user_message: str, style: str = "instruction") -> LLMResult:
        if style == "few_shot":
            prompt = few_shot_prompt(user_message)
        else:
            # default to instruction (never raw)
            prompt = instruction_prompt(user_message)

        reply = f"(stub using {style})\n\nSYSTEM:\n{SYSTEM_PROMPT}\n\nPROMPT:\n{prompt}"
        return LLMResult(reply=reply)