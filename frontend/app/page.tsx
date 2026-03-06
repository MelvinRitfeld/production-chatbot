"use client";

import { useState, useRef, useEffect } from "react";
import { chat } from "@/lib/api";
import type { ChatMessage } from "@/lib/types";

function makeId() {
  return crypto.randomUUID ? crypto.randomUUID() : String(Date.now() + Math.random());
}

const SUGGESTED = [
  "Hoe schrijf ik me in?",
  "Wat kost een abonnement bij BUKU?",
  "Hoe gebruik ik Microsoft Teams?",
  "Wanneer zijn de tentamens?",
];

function TypingIndicator() {
  return (
    <div className="flex items-end gap-3 mb-4">
      <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center text-white text-xs font-bold shrink-0">
        U
      </div>
      <div className="bg-zinc-800 border border-zinc-700 rounded-2xl rounded-bl-sm px-4 py-3">
        <div className="flex gap-1 items-center h-4">
          <span className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
          <span className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
          <span className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
        </div>
      </div>
    </div>
  );
}

function MessageBubble({ msg }: { msg: ChatMessage }) {
  const isUser = msg.role === "user";
  const time = new Date(msg.timestamp).toLocaleTimeString("nl-SR", {
    hour: "2-digit",
    minute: "2-digit",
  });

  if (isUser) {
    return (
      <div className="flex justify-end mb-4">
        <div className="max-w-[75%]">
          <div className="bg-emerald-600 text-white rounded-2xl rounded-br-sm px-4 py-3 text-sm leading-relaxed shadow-lg">
            {msg.content}
          </div>
          <p className="text-xs text-zinc-500 mt-1 text-right">{time}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-end gap-3 mb-4">
      <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center text-white text-xs font-bold shrink-0 shadow">
        U
      </div>
      <div className="max-w-[75%]">
        <div className="bg-zinc-800 border border-zinc-700/60 text-zinc-100 rounded-2xl rounded-bl-sm px-4 py-3 text-sm leading-relaxed shadow">
          {msg.content}
        </div>
        <div className="flex items-center gap-2 mt-1">
          <p className="text-xs text-zinc-500">{time}</p>
          {(msg as any).latency_ms && (
            <p className="text-xs text-zinc-600">{(msg as any).latency_ms}ms</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: makeId(),
      role: "assistant",
      content: "Hallo! Ik ben de UNASAT Campus Assistent. Hoe kan ik je helpen?",
      timestamp: Date.now(),
    },
  ]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isSending]);

  async function handleSend(text: string) {
    if (!text.trim() || isSending) return;
    setInput("");
    setError(null);
    setIsSending(true);

    const userMsg: ChatMessage = {
      id: makeId(),
      role: "user",
      content: text.trim(),
      timestamp: Date.now(),
    };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const res = await chat(text.trim(), conversationId);
      setConversationId(res.conversation_id);
      const botMsg: ChatMessage = {
        id: makeId(),
        role: "assistant",
        content: res.reply,
        timestamp: Date.now(),
        latency_ms: res.latency_ms,
      } as any;
      setMessages((prev) => [...prev, botMsg]);
    } catch (e: any) {
      setError(e?.message ?? "Chat request failed");
    } finally {
      setIsSending(false);
      inputRef.current?.focus();
    }
  }

  function resetChat() {
    setConversationId(null);
    setError(null);
    setInput("");
    setMessages([
      {
        id: makeId(),
        role: "assistant",
        content: "Hallo! Ik ben de UNASAT Campus Assistent. Hoe kan ik je helpen?",
        timestamp: Date.now(),
      },
    ]);
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend(input);
    }
  }

  const showSuggestions = messages.length === 1;

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col">

      {/* Header */}
      <header className="border-b border-zinc-800 bg-zinc-950/90 backdrop-blur-sm sticky top-0 z-10 px-4 py-3">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center font-bold text-sm shadow">
              U
            </div>
            <div>
              <h1 className="text-sm font-semibold text-white leading-none">UNASAT Assistent</h1>
              <p className="text-xs text-emerald-500 mt-0.5">● Online</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <a
              href="/admin"
              className="text-xs text-zinc-400 hover:text-white transition-colors"
            >
              Admin
            </a>
            <button
              onClick={resetChat}
              type="button"
              className="text-xs bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 text-zinc-300 hover:text-white rounded-lg px-3 py-1.5 transition-all"
            >
              + Nieuw gesprek
            </button>
          </div>
        </div>
      </header>

      {/* Messages */}
      <section className="flex-1 overflow-y-auto px-4 py-6">
        <div className="max-w-3xl mx-auto">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} msg={msg} />
          ))}

          {isSending && <TypingIndicator />}

          {error && (
            <div className="mt-2 rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">
              {error}
            </div>
          )}

          {/* Suggested questions */}
          {showSuggestions && !isSending && (
            <div className="mt-6">
              <p className="text-xs text-zinc-500 mb-3 uppercase tracking-wider">Veelgestelde vragen</p>
              <div className="grid grid-cols-2 gap-2">
                {SUGGESTED.map((q) => (
                  <button
                    key={q}
                    onClick={() => handleSend(q)}
                    className="text-left text-sm text-zinc-300 bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 hover:border-emerald-600/50 rounded-xl px-4 py-3 transition-all"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </section>

      {/* Input */}
      <footer className="border-t border-zinc-800 bg-zinc-950 px-4 py-4">
        <div className="max-w-3xl mx-auto">
          <div className="flex items-end gap-3 bg-zinc-900 border border-zinc-700 focus-within:border-emerald-600/60 rounded-2xl px-4 py-3 transition-all">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isSending}
              placeholder="Stel een vraag over UNASAT..."
              rows={1}
              className="flex-1 bg-transparent text-sm text-zinc-100 placeholder-zinc-500 resize-none outline-none max-h-32 leading-relaxed"
              style={{ scrollbarWidth: "none" }}
            />
            <button
              onClick={() => handleSend(input)}
              disabled={isSending || !input.trim()}
              type="button"
              className="shrink-0 w-8 h-8 bg-emerald-600 hover:bg-emerald-500 disabled:bg-zinc-700 disabled:text-zinc-500 text-white rounded-xl flex items-center justify-center transition-all"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            </button>
          </div>
          <p className="text-xs text-zinc-600 mt-2 text-center">
            Enter om te versturen · Shift+Enter voor nieuwe regel
          </p>
        </div>
      </footer>
    </main>
  );
}