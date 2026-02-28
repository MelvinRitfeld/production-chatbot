import type { ChatMessage } from "@/lib/types";

export function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={[
          "max-w-[70%] rounded-2xl px-4 py-3 text-sm",
          isUser ? "bg-zinc-100 text-zinc-900" : "bg-zinc-800 text-zinc-100",
        ].join(" ")}
      >
        <div className="whitespace-pre-wrap">{message.content}</div>

        {!isUser && typeof message.latency_ms === "number" && (
          <div className="mt-2 text-[11px] text-zinc-400">
            Latency: {message.latency_ms} ms
          </div>
        )}
      </div>
    </div>
  );
}