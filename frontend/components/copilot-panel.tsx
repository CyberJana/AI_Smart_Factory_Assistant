"use client";

import { ArrowUp, Bot, LoaderCircle, Sparkles } from "lucide-react";
import { FormEvent, useState } from "react";

import { askCopilot } from "@/lib/api";

export function CopilotPanel() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(
    "I found one priority action: inspect the hydraulic pump vibration on PRESS-02 within the current shift.",
  );
  const [sources, setSources] = useState(["Hydraulic Press Vibration SOP"]);
  const [isLoading, setIsLoading] = useState(false);

  async function submitQuestion(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedQuestion = question.trim();
    if (!trimmedQuestion) return;
    setIsLoading(true);
    try {
      const result = await askCopilot(trimmedQuestion, localStorage.getItem("access_token") ?? undefined);
      setAnswer(result.answer);
      setSources(result.sources);
      setQuestion("");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <article className="panel flex h-full flex-col p-5">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-xl bg-violet-400/10 text-violet-300">
            <Bot size={21} />
          </div>
          <div>
            <p className="font-semibold text-white">Factory Copilot</p>
            <p className="mt-0.5 text-xs text-slate-400">Grounded in operational records</p>
          </div>
        </div>
        <Sparkles className="text-accent" size={18} />
      </div>

      <div className="mt-5 rounded-xl border border-slate-700/70 bg-slate-950/35 p-4">
        <p className="text-sm leading-6 text-slate-200">{answer}</p>
        <div className="mt-3 flex flex-wrap gap-2">
          {sources.map((source) => (
            <span className="rounded-full bg-slate-800 px-2.5 py-1 text-[0.68rem] text-slate-400" key={source}>
              {source}
            </span>
          ))}
        </div>
      </div>

      <div className="mt-5 flex flex-wrap gap-2">
        {["Which machine needs maintenance?", "Why did production drop?", "Explain energy usage"].map((prompt) => (
          <button
            className="rounded-lg border border-slate-700 bg-slate-800/40 px-2.5 py-1.5 text-left text-xs text-slate-300 transition hover:border-accent/40 hover:text-accent"
            key={prompt}
            onClick={() => setQuestion(prompt)}
            type="button"
          >
            {prompt}
          </button>
        ))}
      </div>

      <form className="mt-auto pt-5" onSubmit={submitQuestion}>
        <label className="sr-only" htmlFor="copilot-question">Ask Factory Copilot</label>
        <div className="flex gap-2 rounded-xl border border-slate-700 bg-slate-950/60 p-1.5 focus-within:border-accent/50">
          <input
            className="min-w-0 flex-1 bg-transparent px-2 text-sm text-white outline-none placeholder:text-slate-500"
            id="copilot-question"
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask about your factory..."
            value={question}
          />
          <button
            aria-label="Send question"
            className="grid h-8 w-8 place-items-center rounded-lg bg-accent text-slate-950 transition hover:bg-white disabled:cursor-wait disabled:opacity-60"
            disabled={isLoading}
            type="submit"
          >
            {isLoading ? <LoaderCircle className="animate-spin" size={16} /> : <ArrowUp size={16} />}
          </button>
        </div>
      </form>
    </article>
  );
}
