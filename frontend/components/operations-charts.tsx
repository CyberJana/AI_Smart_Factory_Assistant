"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { TrendPoint } from "@/lib/dashboard";

const tooltipStyle = {
  backgroundColor: "#111b2e",
  border: "1px solid #334155",
  borderRadius: "12px",
  color: "#e6edf8",
};

export function ProductionChart({ data }: { data: TrendPoint[] }) {
  return (
    <article className="panel p-5">
      <div className="mb-5 flex items-start justify-between">
        <div>
          <p className="text-base font-semibold text-white">Production velocity</p>
          <p className="mt-1 text-sm text-slate-400">Actual output against hourly plan</p>
        </div>
        <span className="rounded-full bg-accent/10 px-2.5 py-1 text-xs font-medium text-accent">Live</span>
      </div>
      <div className="h-64">
        <ResponsiveContainer height="100%" width="100%">
          <LineChart data={data} margin={{ left: -18, right: 8 }}>
            <CartesianGrid stroke="#334155" strokeDasharray="3 3" vertical={false} />
            <XAxis axisLine={false} dataKey="label" tick={{ fill: "#94a3b8", fontSize: 12 }} tickLine={false} />
            <YAxis axisLine={false} tick={{ fill: "#94a3b8", fontSize: 12 }} tickLine={false} />
            <Tooltip contentStyle={tooltipStyle} />
            <Legend iconType="circle" wrapperStyle={{ fontSize: "12px" }} />
            <Line dataKey="target" dot={false} name="Target" stroke="#64748b" strokeDasharray="6 5" strokeWidth={2} type="monotone" />
            <Line activeDot={{ r: 5 }} dataKey="actual" dot={false} name="Actual" stroke="#17e5be" strokeWidth={3} type="monotone" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </article>
  );
}

export function EnergyChart({ data }: { data: TrendPoint[] }) {
  return (
    <article className="panel p-5">
      <div className="mb-5">
        <p className="text-base font-semibold text-white">Energy profile</p>
        <p className="mt-1 text-sm text-slate-400">Weekly consumption in kWh</p>
      </div>
      <div className="h-64">
        <ResponsiveContainer height="100%" width="100%">
          <AreaChart data={data} margin={{ left: -18, right: 8 }}>
            <defs>
              <linearGradient id="energyFill" x1="0" x2="0" y1="0" y2="1">
                <stop offset="5%" stopColor="#818cf8" stopOpacity={0.42} />
                <stop offset="95%" stopColor="#818cf8" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#334155" strokeDasharray="3 3" vertical={false} />
            <XAxis axisLine={false} dataKey="label" tick={{ fill: "#94a3b8", fontSize: 12 }} tickLine={false} />
            <YAxis axisLine={false} tick={{ fill: "#94a3b8", fontSize: 12 }} tickLine={false} />
            <Tooltip contentStyle={tooltipStyle} />
            <Area dataKey="kwh" fill="url(#energyFill)" stroke="#818cf8" strokeWidth={2.5} type="monotone" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </article>
  );
}
