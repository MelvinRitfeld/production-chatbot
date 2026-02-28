export type Role = "user" | "assistant";

export type ChatMessage = {
  id: string;
  role: Role;
  content: string;
  timestamp: number; // Date.now()
  latency_ms?: number; // assistant only
};

export type ChatRequest = {
  message: string;
  conversation_id: string | null;
};

export type ChatResponse = {
  reply: string;
  conversation_id: string;
  latency_ms: number;
};

export type MetricsResponse = {
  total_conversations: number;
  avg_latency_ms: number;
  error_count: number;
};