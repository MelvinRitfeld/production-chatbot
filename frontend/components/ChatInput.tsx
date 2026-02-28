import { useState } from "react";

export function ChatInput({
  onSend,
  disabled,
}: {
  onSend: (text: string) => void;
  disabled: boolean;
}) {
  const [text, setText] = useState("");

  function sendNow() {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText("");
  }

  return (
    <div className="flex gap-3">
      <input
        className="flex-1 rounded-xl bg-zinc-900 border border-zinc-800 px-4 py-3 text-sm outline-none focus:border-zinc-600"
        placeholder="Type a message…"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendNow();
          }
        }}
        disabled={disabled}
      />
      <button
        className="rounded-xl bg-zinc-100 px-5 py-3 text-sm font-semibold text-zinc-900 disabled:opacity-60"
        onClick={sendNow}
        disabled={disabled}
        type="button"
      >
        Send
      </button>
    </div>
  );
}