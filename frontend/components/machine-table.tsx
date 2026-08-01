import { ChevronRight } from "lucide-react";

import { Machine, MachineStatus } from "@/lib/dashboard";

const statusStyles: Record<MachineStatus, string> = {
  running: "bg-accent/10 text-accent ring-accent/20",
  warning: "bg-amber-400/10 text-amber-300 ring-amber-300/20",
  maintenance: "bg-blue-400/10 text-blue-300 ring-blue-300/20",
  offline: "bg-slate-500/10 text-slate-300 ring-slate-300/20",
};

export function MachineTable({ machines }: { machines: Machine[] }) {
  return (
    <article className="panel overflow-hidden">
      <div className="flex items-center justify-between px-5 py-5">
        <div>
          <p className="text-base font-semibold text-white">Machine fleet</p>
          <p className="mt-1 text-sm text-slate-400">Live health and utilization by asset</p>
        </div>
        <button className="text-sm font-medium text-accent hover:text-white" type="button">View all assets</button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[650px] text-left text-sm">
          <thead className="border-y border-slate-700/70 bg-slate-950/30 text-xs uppercase tracking-wider text-slate-500">
            <tr>
              <th className="px-5 py-3 font-medium">Asset</th>
              <th className="px-5 py-3 font-medium">Status</th>
              <th className="px-5 py-3 font-medium">Health</th>
              <th className="px-5 py-3 font-medium">Utilization</th>
              <th className="px-5 py-3 font-medium">Location</th>
              <th className="px-5 py-3"><span className="sr-only">Open asset</span></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            {machines.map((machine) => (
              <tr className="transition hover:bg-slate-800/30" key={machine.id}>
                <td className="px-5 py-4">
                  <p className="font-medium text-slate-100">{machine.name}</p>
                  <p className="mt-0.5 text-xs text-slate-500">{machine.code}</p>
                </td>
                <td className="px-5 py-4">
                  <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium capitalize ring-1 ${statusStyles[machine.status]}`}>
                    <span className="h-1.5 w-1.5 rounded-full bg-current" /> {machine.status}
                  </span>
                </td>
                <td className="px-5 py-4">
                  <div className="flex items-center gap-3">
                    <div className="h-1.5 w-24 overflow-hidden rounded-full bg-slate-700">
                      <div className={`h-full rounded-full ${machine.health_score >= 80 ? "bg-accent" : "bg-amber-300"}`} style={{ width: `${machine.health_score}%` }} />
                    </div>
                    <span className="text-slate-300">{machine.health_score}%</span>
                  </div>
                </td>
                <td className="px-5 py-4 text-slate-300">{machine.utilization}%</td>
                <td className="px-5 py-4 text-slate-400">{machine.location}</td>
                <td className="px-5 py-4"><ChevronRight className="text-slate-500" size={18} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </article>
  );
}
