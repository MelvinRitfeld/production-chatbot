from dataclasses import dataclass

from .prompts import SYSTEM_PROMPT, instruction_prompt, few_shot_prompt
from app.services.faq_service import FAQService


@dataclass
class LLMResult:
    reply: str
    model: str = "stub"
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    # tracking fields (optional but useful)
    source: str = "stub"          # "faq" or "stub"
    faq_match_id: str | None = None
    faq_score: int | None = None


class LLMService:
    def __init__(self) -> None:
        self.faq_service = FAQService()

    def generate(self, user_message: str, style: str = "instruction") -> LLMResult:
        """
        Deterministic mode:
        1) Try FAQ match first (returns entry + score).
        2) If not found, fallback to a safe stub reply.
        """

        # 1) FAQ first (IMPORTANT: unpack tuple)
        entry, score = self.faq_service.find_best_match(user_message)

        if entry:
            return LLMResult(
                reply=entry["answer"],
                model="faq",
                source="faq",
                faq_match_id=entry.get("id"),
                faq_score=score,
            )

        # 2) Keep prompt selection (for future real LLM use)
        if style == "few_shot":
            _prompt = few_shot_prompt(user_message)
        else:
            _prompt = instruction_prompt(user_message)

        # 3) Safe fallback (no hallucinations)
        fallback_reply = (
            "Ik kan je vraag momenteel niet met zekerheid beantwoorden.\n"
            "Controleer OneDrive/SHL of neem contact op met info@unasat.sr."
        )

        return LLMResult(
            reply=fallback_reply,
            model="stub",
            source="stub",
            faq_match_id=None,
            faq_score=0,
        )