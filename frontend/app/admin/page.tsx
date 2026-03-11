"use client";

import { useEffect, useState } from "react";
import { getMetrics, getRecentLogs } from "@/lib/api";
import type { MetricsResponse, RecentRequestLog } from "@/lib/types";

function fmtTime(iso: string | null) {
  if (!iso) return "-";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString("nl-SR", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function MetricCard({
  label,
  value,
  sub,
  color = "zinc",
}: {
  label: string;
  value: string | number;
  sub?: string;
  color?: "zinc" | "emerald" | "violet" | "red" | "amber";
}) {
  const accent: Record<string, string> = {
    zinc: "text-white",
    emerald: "text-emerald-400",
    violet: "text-violet-400",
    red: "text-red-400",
    amber: "text-amber-400",
  };
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-4 flex flex-col gap-1">
      <div className="text-xs text-zinc-400">{label}</div>
      <div className={`text-2xl font-semibold ${accent[color]}`}>{value}</div>
      {sub && <div className="text-xs text-zinc-500">{sub}</div>}
    </div>
  );
}

function StatusPill({ code }: { code: number }) {
  const ok = code < 400;
  return (
    <span
      className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${
        ok
          ? "bg-emerald-400/10 text-emerald-400"
          : "bg-red-400/10 text-red-400"
      }`}
    >
      {code}
    </span>
  );
}

function SourcePill({ source }: { source?: string | null }) {
  if (!source) return <span className="text-zinc-600">—</span>;
  if (source === "faq")
    return (
      <span className="inline-flex items-center gap-1 text-xs text-emerald-400">
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block" />
        FAQ
      </span>
    );
  if (source === "llm")
    return (
      <span className="inline-flex items-center gap-1 text-xs text-violet-400">
        <span className="w-1.5 h-1.5 rounded-full bg-violet-400 inline-block" />
        AI
      </span>
    );
  return <span className="text-xs text-zinc-500">{source}</span>;
}

export default function AdminPage() {
  const [data, setData] = useState<MetricsResponse | null>(null);
  const [logs, setLogs] = useState<RecentRequestLog[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastRefresh, setLastRefresh] = useState<Date | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const [m, r] = await Promise.all([getMetrics(), getRecentLogs()]);
      setData(m);
      setLogs(r.logs ?? []);
      setLastRefresh(new Date());
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

      {/* Header */}
      <header className="border-b border-zinc-800 bg-zinc-950/90 backdrop-blur-sm sticky top-0 z-10 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center font-bold text-sm">
              U
            </div>
            <div>
              <h1 className="text-sm font-semibold text-white leading-none">Admin Dashboard</h1>
              <p className="text-xs text-zinc-500 mt-0.5">UNASAT Chatbot Monitoring</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            {lastRefresh && (
              <span className="text-xs text-zinc-600 hidden sm:block">
                Bijgewerkt: {lastRefresh.toLocaleTimeString("nl-SR")}
              </span>
            )}
            <button
              onClick={load}
              disabled={loading}
              type="button"
              className="text-xs bg-zinc-800 hover:bg-zinc-700 disabled:opacity-50 border border-zinc-700 text-zinc-300 hover:text-white rounded-lg px-3 py-1.5 transition-all"
            >
              {loading ? "Laden…" : "↻ Vernieuwen"}
            </button>
            <a
              href="/"
              className="text-xs text-zinc-400 hover:text-white transition-colors"
            >
              ← Terug naar chat
            </a>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-6 space-y-8">

        {error && (
          <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200 flex items-start justify-between gap-4">
            <span>{error}</span>
            <button
              onClick={load}
              className="shrink-0 rounded-lg bg-zinc-100 px-3 py-1.5 text-xs font-semibold text-zinc-900 hover:bg-white"
              type="button"
            >
              Opnieuw
            </button>
          </div>
        )}

        {/* ── Metric cards ── */}
        {data && (
          <section>
            <h2 className="text-xs text-zinc-500 uppercase tracking-wider mb-3">Overzicht</h2>
            <div className="grid gap-3 grid-cols-2 sm:grid-cols-3 lg:grid-cols-6">
              <MetricCard
                label="Gesprekken"
                value={data.total_conversations}
                color="zinc"
              />
              <MetricCard
                label="Berichten"
                value={data.total_messages}
                color="zinc"
              />
              <MetricCard
                label="Gem. latency"
                value={`${Math.round(data.avg_latency_ms)} ms`}
                sub="per verzoek"
                color="amber"
              />
              <MetricCard
                label="Succespercentage"
                value={`${Math.round(data.success_rate * 100)}%`}
                color={data.success_rate >= 0.9 ? "emerald" : "red"}
              />
              <MetricCard
                label="FAQ matches"
                value={(data as any).faq_matches ?? "—"}
                sub={`van ${(data as any).total_chat_requests ?? "?"} vragen`}
                color="emerald"
              />
              <MetricCard
                label="FAQ matchrate"
                value={
                  (data as any).match_rate != null
                    ? `${Math.round((data as any).match_rate * 100)}%`
                    : "—"
                }
                sub="FAQ vs AI"
                color="violet"
              />
            </div>

            {(data.error_count > 0) && (
              <div className="mt-3 rounded-xl border border-amber-500/20 bg-amber-500/10 px-4 py-2.5 text-xs text-amber-300 flex items-center gap-2">
                <span>⚠</span>
                <span>{data.error_count} fout{data.error_count !== 1 ? "en" : ""} geregistreerd in de logs.</span>
              </div>
            )}
          </section>
        )}

        {/* ── Recent requests table ── */}
        <section>
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-xs text-zinc-500 uppercase tracking-wider">Recente verzoeken</h2>
            <span className="text-xs text-zinc-600">{logs.length} items</span>
          </div>

          <div className="overflow-x-auto rounded-2xl border border-zinc-800 bg-zinc-900">
            {loading ? (
              <div className="px-4 py-6 text-sm text-zinc-500">Laden…</div>
            ) : (
              <table className="min-w-full text-sm">
                <thead className="border-b border-zinc-800">
                  <tr>
                    {["Tijd", "Endpoint", "Status", "Bron", "Latency", "Fout"].map((h) => (
                      <th key={h} className="px-4 py-3 text-left text-xs font-medium text-zinc-400">
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {logs.length === 0 ? (
                    <tr>
                      <td className="px-4 py-6 text-zinc-500 text-sm" colSpan={6}>
                        Nog geen logs beschikbaar.
                      </td>
                    </tr>
                  ) : (
                    logs.map((l) => (
                      <tr
                        key={l.id}
                        className="border-b border-zinc-800/60 last:border-0 hover:bg-zinc-800/30 transition-colors"
                      >
                        <td className="px-4 py-3 text-zinc-400 whitespace-nowrap text-xs">
                          {fmtTime(l.created_at)}
                        </td>
                        <td className="px-4 py-3 text-zinc-300 font-mono text-xs">
                          {l.endpoint}
                        </td>
                        <td className="px-4 py-3">
                          <StatusPill code={l.status_code} />
                        </td>
                        <td className="px-4 py-3">
                          <SourcePill source={(l as any).source} />
                        </td>
                        <td className="px-4 py-3 text-zinc-400 text-xs whitespace-nowrap">
                          {l.latency_ms} ms
                        </td>
                        <td className="px-4 py-3 text-zinc-500 text-xs max-w-[200px] truncate">
                          {l.error_message ?? "—"}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            )}
          </div>
        </section>

      </main>
    </div>
  );
}