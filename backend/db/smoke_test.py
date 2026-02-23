import os
from db.crud import (
    create_conversation,
    save_message,
    get_conversation,
    save_request_log,
    get_metrics,
    save_feedback,
)

def main():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set in this terminal session")

    cid = create_conversation()
    print("conversation_id:", cid)

    user_mid = save_message(cid, "user", "hello")
    bot_mid = save_message(cid, "assistant", "hi there!")
    print("user_message_id:", user_mid)
    print("assistant_message_id:", bot_mid)

    convo = get_conversation(cid)
    print("get_conversation():")
    print(convo)

    save_request_log(cid, "/api/chat", 200, 123, None)
    save_request_log(cid, "/api/chat", 500, 50, "boom")
    print("get_metrics():", get_metrics())

    save_feedback(cid, user_mid, 1, "good")
    save_feedback(cid, None, -1, "overall meh")
    print("feedback saved ✅")

if __name__ == "__main__":
    main()