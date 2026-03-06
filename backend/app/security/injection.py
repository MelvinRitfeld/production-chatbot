import re
from dataclasses import dataclass


@dataclass
class InjectionCheckResult:
    is_suspicious: bool
    score: int
    reasons: list[str]


# ── Prompt injection & jailbreak patterns ────────────────────────────────────
_INJECTION_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("role_override",
     re.compile(r"\b(ignore|disregard|override)\b.*\b(system|instructions|rules)\b", re.I)),

    ("ignore_previous",
     re.compile(r"\b(ignore|forget|discard|skip)\b.*\b(previous|above|prior|earlier)\b", re.I)),

    ("system_prompt_exfil",
     re.compile(r"\b(show|reveal|print|leak)\b.*\b(system prompt|hidden prompt|developer message|instructions)\b", re.I)),

    ("jailbreak",
     re.compile(r"\b(jailbreak|do anything now|dan mode|developer mode|unrestricted mode)\b", re.I)),

    ("role_play_attack",
     re.compile(r"\b(pretend|act as)\b.*\b(system|developer|admin|gpt|claude|ai without restrictions)\b", re.I)),

    ("tool_exfil",
     re.compile(r"\b(api key|password|secret|token|credential)\b", re.I)),

    ("instruction_injection",
     re.compile(r"```.*?```", re.S)),

    ("new_instructions",
     re.compile(r"\b(new instruction|updated instruction|your new role|your real instructions)\b", re.I)),

    ("hypothetical_bypass",
     re.compile(r"\b(hypothetically|theoretically|for a story|in fiction|roleplay)\b.*\b(how to|tell me|explain)\b", re.I)),
]

# ── PII patterns (AVG compliance) ────────────────────────────────────────────
_PII_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("email_address",
     re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")),

    ("phone_number",
     re.compile(r"(\+?[0-9]{1,3}[\s\-]?)?(\(?\d{2,4}\)?[\s\-]?)(\d{3,4}[\s\-]?\d{3,4})")),

    ("id_number",
     re.compile(r"\b\d{6,10}\b")),
]


def check_prompt_injection(user_message: str) -> InjectionCheckResult:
    msg = (user_message or "").strip()
    score = 0
    reasons: list[str] = []

    # Check injection patterns
    for name, pattern in _INJECTION_PATTERNS:
        if pattern.search(msg):
            score += 2
            reasons.append(name)

    # Penalize very long messages (possible prompt stuffing)
    if len(msg) > 1200:
        score += 1
        reasons.append("very_long_message")

    # Penalize flood of imperative commands
    imperatives = re.findall(r"\b(do|write|tell|show|give|output|print|list|explain|repeat|say)\b", msg, re.I)
    if len(imperatives) >= 10:
        score += 1
        reasons.append("many_imperatives")

    # Check for ALL CAPS shouting (often used in injection attempts)
    upper_ratio = sum(1 for c in msg if c.isupper()) / max(len(msg), 1)
    if upper_ratio > 0.5 and len(msg) > 20:
        score += 1
        reasons.append("excessive_caps")

    return InjectionCheckResult(
        is_suspicious=score >= 3,
        score=score,
        reasons=reasons
    )


def check_pii(user_message: str) -> list[str]:
    """Returns list of detected PII types. Used for AVG compliance logging."""
    msg = (user_message or "").strip()
    detected = []
    for name, pattern in _PII_PATTERNS:
        if pattern.search(msg):
            detected.append(name)
    return detected