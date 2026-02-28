"use client";

import { useEffect, useState } from "react";
import { getMetrics } from "@/lib/api";
import type { MetricsResponse } from "@/lib/types";

export default function AdminPage() {
  const [data, setData] = useState<MetricsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const res = await getMetrics();
      setData(res);
    } catch (e: any) {
      setError(e?.message ?? "Failed to load metrics");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <header className="border-b border-zinc-800 px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-semibold">Admin Metrics</h1>
          <a href="/" className="text-sm text-zinc-300 hover:text-white underline underline-offset-4">
            Back to Chat
          </a>
        </div>
      </header>

      <main className="px-6 py-6">
        {loading && <div className="text-sm text-zinc-400">Loading…</div>}

        {error && (
          <div className="mb-4 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
            {error}
            <div className="mt-3">
              <button
                onClick={load}
                className="rounded-lg bg-zinc-100 px-3 py-2 text-sm font-semibold text-zinc-900 hover:bg-white"
                type="button"
              >
                Retry
              </button>
            </div>
          </div>
        )}

        {data && (
          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
              <div className="text-xs text-zinc-400">Total conversations</div>
              <div className="mt-2 text-2xl font-semibold">{data.total_conversations}</div>
            </div>

            <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
              <div className="text-xs text-zinc-400">Avg latency (ms)</div>
              <div className="mt-2 text-2xl font-semibold">{Math.round(data.avg_latency_ms)}</div>
            </div>

            <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
              <div className="text-xs text-zinc-400">Error count</div>
              <div className="mt-2 text-2xl font-semibold">{data.error_count}</div>
            </div>
          </div>
        )}

        <div className="mt-6">
          <button
            onClick={load}
            className="rounded-lg bg-zinc-100 px-3 py-2 text-sm font-semibold text-zinc-900 hover:bg-white"
            type="button"
          >
            Refresh
          </button>
        </div>
      </main>
    </div>
  );
}