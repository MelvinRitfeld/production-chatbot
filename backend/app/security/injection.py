import re
from dataclasses import dataclass


@dataclass
class InjectionCheckResult:
    is_suspicious: bool
    score: int
    reasons: list[str]


_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("role_override", re.compile(r"\b(ignore|disregard|override)\b.*\b(system|instructions|rules)\b", re.I)),
    ("system_prompt_exfil", re.compile(r"\b(show|reveal|print|leak)\b.*\b(system prompt|hidden prompt|developer message)\b", re.I)),
    ("jailbreak", re.compile(r"\b(jailbreak|do anything now|dan mode)\b", re.I)),
    ("role_play_attack", re.compile(r"\b(pretend|act as)\b.*\b(system|developer|admin)\b", re.I)),
    ("tool_exfil", re.compile(r"\b(api key|password|secret|token)\b", re.I)),
    ("instruction_injection", re.compile(r"```.*?```", re.S)),
]


def check_prompt_injection(user_message: str) -> InjectionCheckResult:
    msg = (user_message or "").strip()
    score = 0
    reasons: list[str] = []

    for name, pattern in _PATTERNS:
        if pattern.search(msg):
            score += 2
            reasons.append(name)

    if len(msg) > 1200:
        score += 1
        reasons.append("very_long_message")

    imperatives = re.findall(r"\b(do|write|tell|show|give|output|print|list|explain)\b", msg, re.I)
    if len(imperatives) >= 12:
        score += 1
        reasons.append("many_imperatives")

    return InjectionCheckResult(is_suspicious=score >= 3, score=score, reasons=reasons)