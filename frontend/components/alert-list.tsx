import { AlertTriangle, BellRing, Info } from "lucide-react";

import { Alert } from "@/lib/dashboard";

const alertAppearance = {
  critical: { icon: AlertTriangle, styles: "bg-rose-400/10 text-rose-300" },
  high: { icon: AlertTriangle, styles: "bg-amber-400/10 text-amber-300" },
  medium: { icon: BellRing, styles: "bg-blue-400/10 text-blue-300" },
  info: { icon: Info, styles: "bg-slate-400/10 text-slate-300" },
};

export function AlertList({ alerts }: { alerts: Alert[] }) {
  return (
    <article className="panel p-5">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-base font-semibold text-white">Live notifications</p>
          <p className="mt-1 text-sm text-slate-400">Attention needed across the plant</p>
        </div>
        <span className="rounded-full bg-rose-400/10 px-2.5 py-1 text-xs font-semibold text-rose-300">{alerts.length} open</span>
      </div>
      <div className="space-y-3">
        {alerts.map((alert) => {
          const appearance = alertAppearance[alert.severity];
          const Icon = appearance.icon;
          return (
            <div className="flex gap-3 rounded-xl border border-slate-700/70 bg-slate-950/25 p-3" key={alert.id}>
              <div className={`grid h-8 w-8 shrink-0 place-items-center rounded-lg ${appearance.styles}`}>
                <Icon size={16} />
              </div>
              <div className="min-w-0">
                <p className="text-sm font-medium text-slate-200">{alert.title}</p>
                <p className="mt-1 text-xs leading-5 text-slate-400">{alert.message}</p>
              </div>
            </div>
          );
        })}
      </div>
    </article>
  );
}
