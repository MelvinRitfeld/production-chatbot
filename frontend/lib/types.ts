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
  total_messages: number;
  avg_latency_ms: number;
  error_count: number;
  success_rate: number; // 0.0 - 1.0
};


export type RecentRequestLog = {
  id: string;
  endpoint: string;
  status_code: number;
  latency_ms: number;
  error_message: string | null;
  created_at: string | null;
};

export type RecentLogsResponse = {
  logs: RecentRequestLog[];
};