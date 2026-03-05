"use client";

import { useEffect, useState } from "react";
import { getMetrics, getRecentLogs } from "@/lib/api";
import type { MetricsResponse, RecentRequestLog } from "@/lib/types";

function fmtTime(iso: string | null) {
  if (!iso) return "-";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString();
}

export default function AdminPage() {
  const [data, setData] = useState<MetricsResponse | null>(null);
  const [logs, setLogs] = useState<RecentRequestLog[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    setLoading(true);
    setError(null);

    try {
      const [m, r] = await Promise.all([getMetrics(), getRecentLogs()]);
      setData(m);
      setLogs(r.logs ?? []);
    } catch (e: any) {
      setError(e?.message ?? "Failed to load admin data");
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
          <a
            href="/"
            className="text-sm text-zinc-300 hover:text-white underline underline-offset-4"
          >
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
          <>
            <div className="grid gap-4 md:grid-cols-5">
              <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
                <div className="text-xs text-zinc-400">Total conversations</div>
                <div className="mt-2 text-2xl font-semibold">
                  {data.total_conversations}
                </div>
              </div>

              <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
                <div className="text-xs text-zinc-400">Total messages</div>
                <div className="mt-2 text-2xl font-semibold">
                  {data.total_messages}
                </div>
              </div>

              <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
                <div className="text-xs text-zinc-400">Avg latency (ms)</div>
                <div className="mt-2 text-2xl font-semibold">
                  {Math.round(data.avg_latency_ms)}
                </div>
              </div>

              <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
                <div className="text-xs text-zinc-400">Error count</div>
                <div className="mt-2 text-2xl font-semibold">
                  {data.error_count}
                </div>
              </div>

              <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
                <div className="text-xs text-zinc-400">Success rate</div>
                <div className="mt-2 text-2xl font-semibold">
                  {Math.round(data.success_rate * 100)}%
                </div>
              </div>
            </div>

            <p className="mt-4 text-sm text-zinc-400">
              These metrics help us evaluate system performance and reliability during testing.
            </p>
          </>
        )}

        {/* Recent Requests */}
        <section className="mt-8">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-semibold">Recent Requests</h2>
            <button
              onClick={load}
              className="rounded-lg bg-zinc-100 px-3 py-2 text-sm font-semibold text-zinc-900 hover:bg-white"
              type="button"
            >
              Refresh
            </button>
          </div>

          <div className="mt-3 overflow-x-auto rounded-2xl border border-zinc-800 bg-zinc-900">
            <table className="min-w-full text-sm">
              <thead className="border-b border-zinc-800 text-zinc-300">
                <tr>
                  <th className="px-4 py-3 text-left font-medium">Time</th>
                  <th className="px-4 py-3 text-left font-medium">Endpoint</th>
                  <th className="px-4 py-3 text-left font-medium">Status</th>
                  <th className="px-4 py-3 text-left font-medium">Latency</th>
                  <th className="px-4 py-3 text-left font-medium">Error</th>
                </tr>
              </thead>
              <tbody>
                {logs.length === 0 ? (
                  <tr>
                    <td className="px-4 py-4 text-zinc-400" colSpan={5}>
                      No logs yet.
                    </td>
                  </tr>
                ) : (
                  logs.map((l) => (
                    <tr key={l.id} className="border-b border-zinc-800 last:border-0">
                      <td className="px-4 py-3 text-zinc-300">{fmtTime(l.created_at)}</td>
                      <td className="px-4 py-3">{l.endpoint}</td>
                      <td className="px-4 py-3">{l.status_code}</td>
                      <td className="px-4 py-3">{l.latency_ms} ms</td>
                      <td className="px-4 py-3 text-zinc-400">
                        {l.error_message ? l.error_message : "-"}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}