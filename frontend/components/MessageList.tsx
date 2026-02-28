import type { ChatMessage } from "@/lib/types";
import { MessageBubble } from "./MessageBubble";

export function MessageList({
  messages,
  isSending,
}: {
  messages: ChatMessage[];
  isSending: boolean;
}) {
  return (
    <div className="space-y-4">
      {messages.map((m) => (
        <MessageBubble key={m.id} message={m} />
      ))}

      {isSending && (
        <div className="text-xs text-zinc-400">Sending…</div>
      )}
    </div>
  );
}