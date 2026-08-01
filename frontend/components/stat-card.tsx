import { ArrowDownRight, ArrowUpRight, type LucideIcon } from "lucide-react";

interface StatCardProps {
  label: string;
  value: string;
  detail: string;
  change?: string;
  trend?: "up" | "down";
  icon: LucideIcon;
  accent?: "mint" | "blue" | "amber" | "rose";
}

const accentStyles = {
  mint: "bg-accent/10 text-accent",
  blue: "bg-blue-400/10 text-blue-300",
  amber: "bg-amber-400/10 text-amber-300",
  rose: "bg-rose-400/10 text-rose-300",
};

export function StatCard({
  label,
  value,
  detail,
  change,
  trend = "up",
  icon: Icon,
  accent = "mint",
}: StatCardProps) {
  const TrendIcon = trend === "up" ? ArrowUpRight : ArrowDownRight;
  const trendStyle = trend === "up" ? "text-accent" : "text-amber-300";
  return (
    <article className="panel p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="eyebrow">{label}</p>
          <p className="mt-3 text-3xl font-semibold tracking-tight text-white">{value}</p>
        </div>
        <span className={`grid h-10 w-10 place-items-center rounded-xl ${accentStyles[accent]}`}>
          <Icon size={20} />
        </span>
      </div>
      <div className="mt-5 flex items-center gap-2 text-xs">
        {change && (
          <span className={`inline-flex items-center font-semibold ${trendStyle}`}>
            <TrendIcon size={14} /> {change}
          </span>
        )}
        <span className="text-slate-500">{detail}</span>
      </div>
    </article>
  );
}
