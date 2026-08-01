"use client";

import {
  Activity,
  BarChart3,
  Boxes,
  Bot,
  BrainCircuit,
  ClipboardList,
  Factory,
  Gauge,
  PackageSearch,
  Settings,
  ShieldCheck,
  Zap,
} from "lucide-react";
import { useState } from "react";

const primaryNavigation = [
  { label: "Command Center", icon: Gauge },
  { label: "Machine Monitoring", icon: Activity },
  { label: "Predictive Maintenance", icon: BrainCircuit },
  { label: "Quality Vision", icon: ShieldCheck },
  { label: "Production", icon: Factory },
  { label: "Inventory", icon: PackageSearch },
  { label: "Energy", icon: Zap },
  { label: "Analytics", icon: BarChart3 },
];

export function Sidebar() {
  const [activeItem, setActiveItem] = useState("Command Center");

  return (
    <aside className="hidden min-h-screen w-72 shrink-0 border-r border-slate-700/70 bg-slate-950/50 px-4 py-6 lg:block">
      <div className="mb-9 flex items-center gap-3 px-3">
        <div className="grid h-10 w-10 place-items-center rounded-xl bg-accent text-slate-950 shadow-[0_0_26px_rgba(23,229,190,0.35)]">
          <Boxes size={22} strokeWidth={2.8} />
        </div>
        <div>
          <p className="font-semibold tracking-tight text-white">ForgeSight</p>
          <p className="text-xs text-slate-400">Factory intelligence</p>
        </div>
      </div>

      <p className="eyebrow mb-3 px-3">Operations</p>
      <nav className="space-y-1">
        {primaryNavigation.map(({ label, icon: Icon }) => {
          const isActive = activeItem === label;
          return (
            <button
              className={`flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition ${
                isActive
                  ? "bg-accent/10 font-medium text-accent"
                  : "text-slate-400 hover:bg-slate-800/70 hover:text-slate-100"
              }`}
              key={label}
              onClick={() => setActiveItem(label)}
              type="button"
            >
              <Icon size={18} />
              {label}
            </button>
          );
        })}
      </nav>

      <p className="eyebrow mb-3 mt-8 px-3">Workspace</p>
      <nav className="space-y-1">
        <button className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-slate-400 hover:bg-slate-800/70 hover:text-slate-100" type="button">
          <ClipboardList size={18} /> Reports
        </button>
        <button className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-slate-400 hover:bg-slate-800/70 hover:text-slate-100" type="button">
          <Bot size={18} /> AI Copilot
        </button>
        <button className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm text-slate-400 hover:bg-slate-800/70 hover:text-slate-100" type="button">
          <Settings size={18} /> Settings
        </button>
      </nav>

      <div className="mt-10 rounded-2xl border border-accent/20 bg-accent/5 p-4">
        <p className="text-sm font-semibold text-white">Systems online</p>
        <p className="mt-1 text-xs leading-5 text-slate-400">Telemetry is synchronized across 4 connected assets.</p>
        <div className="mt-3 flex items-center gap-2 text-xs font-medium text-accent">
          <span className="h-2 w-2 rounded-full bg-accent" /> All services healthy
        </div>
      </div>
    </aside>
  );
}
