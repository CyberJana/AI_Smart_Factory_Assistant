"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("admin@smartfactory.example");
  const [password, setPassword] = useState("ChangeMe123!");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function login(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${apiUrl}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!response.ok) throw new Error("Invalid email or password.");
      const tokens = await response.json() as { access_token: string; refresh_token: string };
      localStorage.setItem("access_token", tokens.access_token);
      localStorage.setItem("refresh_token", tokens.refresh_token);
      router.push("/");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Unable to sign in.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="grid min-h-screen place-items-center px-4">
      <section className="panel w-full max-w-md p-8">
        <p className="eyebrow">ForgeSight secure access</p>
        <h1 className="mt-2 text-3xl font-semibold text-white">Welcome back</h1>
        <p className="mt-2 text-sm text-slate-400">Sign in to access your factory command center.</p>
        <form className="mt-7 space-y-4" onSubmit={login}>
          <label className="block text-sm text-slate-300">Work email
            <input className="mt-1.5 w-full rounded-xl border border-slate-700 bg-slate-950/70 px-3 py-2.5 outline-none focus:border-accent" onChange={(event) => setEmail(event.target.value)} type="email" value={email} />
          </label>
          <label className="block text-sm text-slate-300">Password
            <input className="mt-1.5 w-full rounded-xl border border-slate-700 bg-slate-950/70 px-3 py-2.5 outline-none focus:border-accent" onChange={(event) => setPassword(event.target.value)} type="password" value={password} />
          </label>
          {error && <p className="text-sm text-rose-300">{error}</p>}
          <button className="w-full rounded-xl bg-accent py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-white disabled:opacity-60" disabled={loading} type="submit">
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>
        <p className="mt-5 text-xs leading-5 text-slate-500">Demo credentials are prefilled. Change them before any non-demo deployment.</p>
      </section>
    </main>
  );
}
