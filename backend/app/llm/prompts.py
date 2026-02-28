SYSTEM_PROMPT = "You are a helpful assistant for a campus support chatbot."

def instruction_prompt(user_message: str) -> str:
    return f"Answer the user's question clearly and safely.\n\nUser: {user_message}"

def few_shot_prompt(user_message: str) -> str:
    return (
        "Example:\n"
        "User: What are the opening hours?\n"
        "Assistant: The campus is open from 8:00 to 16:00.\n\n"
        f"User: {user_message}\n"
        "Assistant:"
    )