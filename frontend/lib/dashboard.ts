export type MachineStatus = "running" | "warning" | "maintenance" | "offline";

export interface Machine {
  id: string;
  code: string;
  name: string;
  location: string;
  status: MachineStatus;
  health_score: number;
  utilization: number;
}

export interface Alert {
  id: string;
  title: string;
  severity: "critical" | "high" | "medium" | "info";
  message: string;
}

export interface TrendPoint {
  label: string;
  actual?: number;
  target?: number;
  kwh?: number;
}

export interface DashboardData {
  kpis: {
    oee: number;
    production_today: number;
    production_target: number;
    running_machines: number;
    machine_count: number;
    energy_kwh: number;
    quality_score: number;
    rejected_products: number;
    open_alerts: number;
    low_stock_items: number;
  };
  machines: Machine[];
  alerts: Alert[];
  production_trend: TrendPoint[];
  energy_trend: TrendPoint[];
}

export const demoDashboard: DashboardData = {
  kpis: {
    oee: 84.6,
    production_today: 1820,
    production_target: 2400,
    running_machines: 2,
    machine_count: 4,
    energy_kwh: 949.2,
    quality_score: 98.2,
    rejected_products: 1,
    open_alerts: 2,
    low_stock_items: 1,
  },
  machines: [
    { id: "1", code: "CNC-01", name: "CNC Milling Cell 01", location: "Assembly A", status: "running", health_score: 96, utilization: 89 },
    { id: "2", code: "PRESS-02", name: "Hydraulic Press 02", location: "Forming B", status: "warning", health_score: 68, utilization: 72 },
    { id: "3", code: "ROBOT-04", name: "Welding Robot 04", location: "Assembly A", status: "running", health_score: 92, utilization: 94 },
    { id: "4", code: "PACK-03", name: "Packaging Station 03", location: "Packaging", status: "maintenance", health_score: 55, utilization: 0 },
  ],
  alerts: [
    { id: "1", severity: "high", title: "High vibration on PRESS-02", message: "34% above operating baseline; inspect within one shift." },
    { id: "2", severity: "info", title: "Maintenance window active", message: "PACK-03 conveyor replacement in progress." },
  ],
  production_trend: [
    { label: "06:00", actual: 240, target: 260 },
    { label: "08:00", actual: 510, target: 520 },
    { label: "10:00", actual: 760, target: 780 },
    { label: "12:00", actual: 1030, target: 1040 },
    { label: "14:00", actual: 1820, target: 2400 },
  ],
  energy_trend: [
    { label: "Mon", kwh: 1200 },
    { label: "Tue", kwh: 1110 },
    { label: "Wed", kwh: 1260 },
    { label: "Thu", kwh: 1180 },
    { label: "Fri", kwh: 949 },
  ],
};
