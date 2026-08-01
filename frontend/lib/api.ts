import { DashboardData, demoDashboard } from "@/lib/dashboard";

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export async function getDashboard(accessToken?: string): Promise<DashboardData> {
  if (!accessToken) return demoDashboard;

  const response = await fetch(`${apiUrl}/analytics/dashboard`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!response.ok) throw new Error("Unable to load live factory data");
  return response.json() as Promise<DashboardData>;
}

export async function askCopilot(question: string, accessToken?: string) {
  if (!accessToken) {
    return {
      answer:
        "Priority action: Inspect hydraulic pump vibration. PRESS-02 is 34% above its operating baseline.",
      sources: ["Hydraulic Press Vibration SOP"],
    };
  }
  const response = await fetch(`${apiUrl}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${accessToken}` },
    body: JSON.stringify({ question }),
  });
  if (!response.ok) throw new Error("The factory copilot could not answer this request");
  return response.json() as Promise<{ answer: string; sources: string[] }>;
}
