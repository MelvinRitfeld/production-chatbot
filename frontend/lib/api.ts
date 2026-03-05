import type { ChatRequest, ChatResponse, MetricsResponse, RecentLogsResponse } from "./types";

const RAW_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

if (!RAW_BASE) {
  throw new Error("Missing NEXT_PUBLIC_API_BASE_URL. Set it in frontend/.env.local");
}

const API_BASE = RAW_BASE.replace(/\/$/, "");

async function readError(res: Response) {
  const text = await res.text().catch(() => "");
  return text || res.statusText;
}

export async function chat(
  message: string,
  conversation_id: string | null = null
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, conversation_id } satisfies ChatRequest),
  });

  if (!res.ok) {
    throw new Error(`Chat failed (${res.status}): ${await readError(res)}`);
  }

  return res.json();
}

export async function getMetrics(): Promise<MetricsResponse> {
  const res = await fetch(`${API_BASE}/api/admin/metrics`, {
    method: "GET",
    headers: { Accept: "application/json" },
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Metrics failed (${res.status}): ${await readError(res)}`);
  }

  return res.json();
}



export async function getRecentLogs(): Promise<RecentLogsResponse> {
  const res = await fetch(`${API_BASE}/api/admin/recent`, {
    method: "GET",
    headers: { Accept: "application/json" },
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`Recent logs failed (${res.status}): ${await readError(res)}`);
  }

  return res.json();
}