def safe_fallback_response() -> str:
    """Returned when prompt injection or jailbreak is detected."""
    return (
        "Ik kan niet helpen met verzoeken die proberen de systeemregels te omzeilen "
        "of verborgen instructies te onthullen. "
        "Als je een gewone vraag hebt over UNASAT, help ik je graag verder."
    )


def out_of_scope_response() -> str:
    """Returned when the question is clearly outside UNASAT scope."""
    return (
        "Deze vraag valt buiten wat ik als UNASAT Campus Assistent kan beantwoorden. "
        "Ik help je graag met vragen over inschrijving, roosters, Microsoft Teams, "
        "toetsen en algemene campusinformatie."
    )


def api_error_response() -> str:
    """Returned when the Groq API call fails."""
    return (
        "Ik kan je vraag momenteel niet beantwoorden vanwege een technisch probleem. "
        "Probeer het later opnieuw of neem contact op via info@unasat.sr."
    )


def rate_limit_response() -> str:
    """Returned when the user is sending too many messages too quickly."""
    return (
        "Je stuurt te veel berichten achter elkaar. "
        "Wacht even en probeer het daarna opnieuw."
    )


def empty_input_response() -> str:
    """Returned when the user sends an empty or whitespace-only message."""
    return "Je bericht is leeg. Stel gerust een vraag over UNASAT!"