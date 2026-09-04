"use client";
import React from "react";
import { motion } from "motion/react";
import { Badge } from "@/components/ui/badge";
import {
  MousePointerClick,
  ArrowDown,
  Type,
  ScrollText,
  Timer,
  XCircle,
  CheckCircle2,
  Bot,
  FileText,
  Zap,
} from "lucide-react";

export const NotABrowserSection = () => {
  const wrongSteps = [
    { icon: MousePointerClick, label: "Click" },
    { icon: Type, label: "Type" },
    { icon: ScrollText, label: "Scroll" },
    { icon: Timer, label: "Wait" },
    { icon: MousePointerClick, label: "Click again" },
    { icon: ScrollText, label: "Extract" },
  ];

  return (
    <section className="relative py-24 sm:py-32 border-b border-zinc-900 bg-zinc-950/40 overflow-hidden">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 text-center">
        <Badge variant="secondary" className="mb-4">
          Architecture Philosophy
        </Badge>
        <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white">
          We don&apos;t give your agent a browser.
        </h2>
        <p className="mt-4 text-zinc-400 max-w-2xl mx-auto text-base sm:text-lg">
          Because a browser is a tool for humans. An agent needs a retrieval interface.
        </p>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* ❌ The Wrong Way: Browser Agent */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="rounded-2xl border border-red-900/50 bg-red-950/10 p-6 sm:p-8 text-left relative overflow-hidden"
          >
            {/* Desaturated overlay */}
            <div className="absolute inset-0 bg-zinc-950/30 pointer-events-none" />

            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-6">
                <div className="h-10 w-10 rounded-xl bg-red-950/60 border border-red-800/50 flex items-center justify-center">
                  <XCircle className="h-5 w-5 text-red-400" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-red-300">Browser Agent</h3>
                  <p className="text-xs text-red-400/60 font-mono">Fragile, slow, unreliable</p>
                </div>
              </div>

              <div className="space-y-3">
                {wrongSteps.map((step, idx) => {
                  const Icon = step.icon;
                  return (
                    <div
                      key={idx}
                      className="flex items-center gap-3 text-sm text-zinc-500"
                    >
                      <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded bg-zinc-900/80 border border-zinc-800">
                        <Icon className="h-3.5 w-3.5 text-zinc-600" />
                      </div>
                      <span className="font-mono">{step.label}</span>
                      {idx < wrongSteps.length - 1 && (
                        <ArrowDown className="h-3 w-3 text-zinc-700 ml-auto" />
                      )}
                    </div>
                  );
                })}
              </div>

              <div className="mt-6 pt-4 border-t border-red-900/30">
                <p className="text-xs text-red-400/80 font-mono">
                  6 brittle operations. Any DOM change breaks it.
                </p>
              </div>
            </div>
          </motion.div>

          {/* ✅ The Right Way: ContextPortal */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.15 }}
            className="rounded-2xl border border-emerald-500/30 bg-emerald-950/10 p-6 sm:p-8 text-left relative overflow-hidden"
          >
            {/* Slight glow */}
            <div className="absolute -top-20 -right-20 w-40 h-40 bg-emerald-500/8 blur-[80px] pointer-events-none" />

            <div className="relative z-10">
              <div className="flex items-center gap-3 mb-6">
                <div className="h-10 w-10 rounded-xl bg-emerald-950/80 border border-emerald-500/40 flex items-center justify-center">
                  <CheckCircle2 className="h-5 w-5 text-emerald-400" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-emerald-300">ContextPortal</h3>
                  <p className="text-xs text-emerald-400/60 font-mono">One semantic call</p>
                </div>
              </div>

              <div className="space-y-5">
                <div className="flex items-center gap-3 text-sm">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-blue-950/60 border border-blue-500/30">
                    <Bot className="h-4 w-4 text-blue-400" />
                  </div>
                  <div>
                    <span className="text-zinc-200 font-mono text-sm">
                      &quot;Give me the context from this URL.&quot;
                    </span>
                  </div>
                </div>

                <div className="flex justify-center">
                  <div className="h-8 w-px bg-gradient-to-b from-blue-500/50 to-emerald-500/50" />
                </div>

                <div className="flex items-center gap-3 text-sm">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-purple-950/60 border border-purple-500/30">
                    <Zap className="h-4 w-4 text-purple-400" />
                  </div>
                  <div>
                    <span className="text-zinc-400 font-mono text-xs">ContextPortal handles everything internally</span>
                  </div>
                </div>

                <div className="flex justify-center">
                  <div className="h-8 w-px bg-gradient-to-b from-purple-500/50 to-emerald-500/50" />
                </div>

                <div className="flex items-center gap-3 text-sm">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-emerald-950/60 border border-emerald-500/30">
                    <FileText className="h-4 w-4 text-emerald-400" />
                  </div>
                  <div>
                    <span className="text-emerald-300 font-mono text-sm font-semibold">
                      Clean Markdown context returned ✅
                    </span>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-emerald-500/20">
                <p className="text-xs text-emerald-400/80 font-mono">
                  1 semantic operation. DOM-agnostic. Never breaks.
                </p>
              </div>
            </div>
          </motion.div>
        </div>

        {/* The Key Line */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="mt-16"
        >
          <p className="text-xl sm:text-2xl font-bold text-white max-w-2xl mx-auto">
            Give your agent a retrieval tool,{" "}
            <span className="bg-gradient-to-r from-blue-400 to-emerald-400 bg-clip-text text-transparent">
              not a browser to operate.
            </span>
          </p>
        </motion.div>
      </div>
    </section>
  );
};
