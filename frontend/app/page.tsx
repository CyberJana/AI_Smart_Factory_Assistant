"use client";

import { useQuery } from "@tanstack/react-query";
import { Bell, ChevronDown, CircleHelp, Factory, Menu, Search, ShieldAlert, Target, Zap } from "lucide-react";

import { AlertList } from "@/components/alert-list";
import { CopilotPanel } from "@/components/copilot-panel";
import { MachineTable } from "@/components/machine-table";
import { EnergyChart, ProductionChart } from "@/components/operations-charts";
import { Sidebar } from "@/components/sidebar";
import { StatCard } from "@/components/stat-card";
import { getDashboard } from "@/lib/api";

export default function CommandCenter() {
  const { data, isFetching } = useQuery({
    queryKey: ["dashboard"],
    queryFn: () => getDashboard(typeof window === "undefined" ? undefined : localStorage.getItem("access_token") ?? undefined),
  });

  if (!data) return null;
  const { kpis } = data;

  return (
    <div className="min-h-screen lg:flex">
      <Sidebar />
      <main className="min-w-0 flex-1 px-4 py-4 sm:px-6 lg:px-8 lg:py-6">
        <header className="mb-7 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <button className="grid h-10 w-10 place-items-center rounded-xl border border-slate-700 bg-slate-900 lg:hidden" type="button">
              <Menu size={19} />
            </button>
            <div>
              <div className="flex items-center gap-2">
                <p className="eyebrow">Northstar Manufacturing / Plant 01</p>
                <span className="h-1.5 w-1.5 rounded-full bg-accent" />
              </div>
              <h1 className="mt-1 text-2xl font-semibold tracking-tight text-white sm:text-3xl">Command Center</h1>
            </div>
          </div>
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="hidden h-10 w-60 items-center gap-2 rounded-xl border border-slate-700 bg-slate-900/70 px-3 sm:flex">
              <Search size={17} className="text-slate-500" />
              <input aria-label="Search factory data" className="w-full bg-transparent text-sm outline-none placeholder:text-slate-500" placeholder="Search assets, orders..." />
            </div>
            <button aria-label="Help" className="grid h-10 w-10 place-items-center rounded-xl border border-slate-700 bg-slate-900/70 text-slate-300 hover:text-white" type="button"><CircleHelp size={18} /></button>
            <button aria-label="Notifications" className="relative grid h-10 w-10 place-items-center rounded-xl border border-slate-700 bg-slate-900/70 text-slate-300 hover:text-white" type="button">
              <Bell size={18} /><span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-rose-400" />
            </button>
            <button className="flex h-10 items-center gap-2 rounded-xl border border-slate-700 bg-slate-900/70 px-2 text-sm" type="button">
              <span className="grid h-6 w-6 place-items-center rounded-lg bg-accent font-bold text-slate-950">AM</span>
              <ChevronDown size={15} className="text-slate-500" />
            </button>
          </div>
        </header>

        <section className="mb-7 flex flex-wrap items-end justify-between gap-3">
          <div>
            <p className="text-sm text-slate-400">Friday, August 1, 2026 <span className="mx-2 text-slate-600">|</span> Shift 1 in progress</p>
          </div>
          <span className="inline-flex items-center gap-2 rounded-full border border-accent/20 bg-accent/5 px-3 py-1.5 text-xs font-medium text-accent">
            <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-accent" /> {isFetching ? "Syncing telemetry" : "Telemetry synchronized"}
          </span>
        </section>

        <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard accent="mint" change="+2.4%" detail="vs. yesterday" icon={Target} label="Overall OEE" value={`${kpis.oee}%`} />
          <StatCard accent="blue" change={`${kpis.production_today.toLocaleString()} units`} detail={`of ${kpis.production_target.toLocaleString()} target`} icon={Factory} label="Today's production" value={`${Math.round((kpis.production_today / kpis.production_target) * 100)}%`} />
          <StatCard accent="amber" detail={`${kpis.running_machines} of ${kpis.machine_count} assets online`} icon={ShieldAlert} label="Fleet availability" trend="down" value={`${kpis.running_machines}/${kpis.machine_count}`} />
          <StatCard accent="rose" change="-4.8%" detail="vs. weekly average" icon={Zap} label="Energy consumed" value={`${kpis.energy_kwh.toLocaleString()} kWh`} />
        </section>

        <section className="mt-5 grid gap-5 xl:grid-cols-[minmax(0,1.75fr)_minmax(300px,0.95fr)]">
          <ProductionChart data={data.production_trend} />
          <CopilotPanel />
        </section>

        <section className="mt-5 grid gap-5 xl:grid-cols-[minmax(0,1.75fr)_minmax(300px,0.95fr)]">
          <MachineTable machines={data.machines} />
          <AlertList alerts={data.alerts} />
        </section>

        <section className="mt-5 pb-4">
          <EnergyChart data={data.energy_trend} />
        </section>
      </main>
    </div>
  );
}
