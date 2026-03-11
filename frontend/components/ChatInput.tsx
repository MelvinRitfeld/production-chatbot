import { useState, useRef, useEffect } from "react";

const MAX_CHARS = 500;

export function ChatInput({
  onSend,
  disabled,
}: {
  onSend: (text: string) => void;
  disabled: boolean;
}) {
  const [text, setText] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea height as user types
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 128) + "px";
  }, [text]);

  const isOverLimit = text.length > MAX_CHARS;
  const showCounter = text.length > MAX_CHARS * 0.8;

  function sendNow() {
    const trimmed = text.trim();
    if (!trimmed || disabled || isOverLimit) return;
    onSend(trimmed);
    setText("");
  }

  return (
    <div className="flex flex-col gap-1">
      <div className={`flex gap-3 items-end rounded-xl border px-4 py-3 transition-all ${
        isOverLimit
          ? "border-red-500/60 bg-zinc-900"
          : "border-zinc-800 bg-zinc-900 focus-within:border-zinc-600"
      }`}>
        <textarea
          ref={textareaRef}
          className="flex-1 bg-transparent text-sm text-zinc-100 placeholder-zinc-500 resize-none outline-none max-h-32 leading-relaxed"
          placeholder="Stel een vraag over UNASAT..."
          value={text}
          rows={1}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              sendNow();
            }
          }}
          disabled={disabled}
          style={{ scrollbarWidth: "none" }}
        />
        <button
          className="rounded-xl bg-zinc-100 px-5 py-3 text-sm font-semibold text-zinc-900 disabled:opacity-60 shrink-0 transition-opacity"
          onClick={sendNow}
          disabled={disabled || !text.trim() || isOverLimit}
          type="button"
        >
          Send
        </button>
      </div>

      <div className="flex justify-between items-center px-1">
        <span className="text-xs text-zinc-600">Enter om te versturen · Shift+Enter voor nieuwe regel</span>
        {showCounter && (
          <span className={`text-xs ${isOverLimit ? "text-red-400 font-medium" : "text-zinc-500"}`}>
            {text.length}/{MAX_CHARS}
          </span>
        )}
      </div>

      {isOverLimit && (
        <p className="text-xs text-red-400 px-1">
          Je bericht is te lang. Max {MAX_CHARS} tekens.
        </p>
      )}
    </div>
  );
}