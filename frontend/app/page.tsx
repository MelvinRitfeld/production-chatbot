"use client";

import { useState } from "react";
import { chat } from "@/lib/api";
import type { ChatMessage } from "@/lib/types";

import { ChatInput } from "@/components/ChatInput";
import { MessageList } from "@/components/MessageList";

function makeId() {
  return crypto.randomUUID ? crypto.randomUUID() : String(Date.now() + Math.random());
}

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { id: makeId(), role: "assistant", content: "Hi! Ask me something.", timestamp: Date.now() },
  ]);

  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSend(text: string) {
    if (isSending) return;

    setError(null);
    setIsSending(true);

    const userMsg: ChatMessage = {
      id: makeId(),
      role: "user",
      content: text,
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const res = await chat(text, conversationId);
      setConversationId(res.conversation_id);

      const botMsg: ChatMessage = {
        id: makeId(),
        role: "assistant",
        content: res.reply,
        timestamp: Date.now(),
        latency_ms: res.latency_ms,
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (e: any) {
      setError(e?.message ?? "Chat request failed");
    } finally {
      setIsSending(false);
    }
  }

  function resetChat() {
    setConversationId(null);
    setError(null);
    setMessages([
      { id: makeId(), role: "assistant", content: "New chat started. Ask me something.", timestamp: Date.now() },
    ]);
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col">
      <header className="border-b border-zinc-800 px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-semibold">Chat</h1>
          <div className="flex gap-3 items-center">
            <a
              href="/admin"
              className="text-sm text-zinc-300 hover:text-white underline underline-offset-4"
            >
              Admin
            </a>
            <button
              onClick={resetChat}
              className="text-sm rounded-lg bg-zinc-100 px-3 py-2 text-zinc-900 hover:bg-white"
              type="button"
            >
              New chat
            </button>
          </div>
        </div>
      </header>

      <section className="flex-1 px-6 py-6 overflow-y-auto">
        <MessageList messages={messages} isSending={isSending} />

        {error && (
          <div className="mt-4 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
            {error}
          </div>
        )}
      </section>

      <footer className="border-t border-zinc-800 px-6 py-4">
        <ChatInput onSend={handleSend} disabled={isSending} />
        <div className="mt-2 text-xs text-zinc-500">
          Press Enter to send. Shift+Enter for newline.
        </div>
      </footer>
    </main>
  );
}