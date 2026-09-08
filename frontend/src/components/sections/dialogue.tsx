"use client";
import React from "react";
import { motion } from "motion/react";
import { Badge } from "@/ui/badge";
import { Bot, User, CheckCircle2, MessageSquare } from "lucide-react";

export const DialogueSection = () => {
  return (
    <section className="relative py-24 sm:py-32 border-b border-zinc-900 bg-zinc-950/60 overflow-hidden">
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 text-center">
        <Badge variant="glow" className="mb-4">
          Core Workflow
        </Badge>
        <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white">
          So… what exactly happens?
        </h2>
        <p className="mt-4 text-zinc-400 max-w-xl mx-auto text-base sm:text-lg">
          Authenticate once in your browser. Retrieve context continuously without interrupting your day.
        </p>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-2 gap-8 text-left">
          {/* Conversation 1: First Time */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="rounded-2xl border border-zinc-800 bg-zinc-900/40 p-6 sm:p-8 backdrop-blur-md flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-zinc-800">
                <span className="font-bold text-white flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-blue-500" />
                  Day 1: The First Time
                </span>
                <span className="text-xs font-mono text-zinc-500">
                  Initial Authentication
                </span>
              </div>

              <div className="space-y-4 text-sm font-mono">
                <div className="flex items-start gap-3">
                  <span className="text-blue-400 font-semibold shrink-0">🤖 Agent:</span>
                  <span className="text-zinc-300">
                    &quot;I need the internal roadmaps from confluence.corp.com/q3.&quot;
                  </span>
                </div>

                <div className="flex items-start gap-3">
                  <span className="text-purple-400 font-semibold shrink-0">◉ Portal:</span>
                  <span className="text-zinc-400">
                    &quot;It&apos;s behind Okta SSO. Opening your browser...&quot;
                  </span>
                </div>

                <div className="flex items-start gap-3 bg-zinc-800/40 p-2.5 rounded-lg border border-zinc-700/50">
                  <span className="text-amber-400 font-semibold shrink-0">👤 You:</span>
                  <span className="text-zinc-200">
                    *Taps TouchID / Enters 2FA once in local Chromium*
                  </span>
                </div>

                <div className="flex items-start gap-3">
                  <span className="text-emerald-400 font-semibold shrink-0">◉ Portal:</span>
                  <span className="text-zinc-300">
                    &quot;Nice. Session saved securely to local profile. Context delivered.&quot; ✅
                  </span>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-zinc-800/60 text-xs text-zinc-500">
              One-time interactive setup for protected hosts.
            </div>
          </motion.div>

          {/* Conversation 2: Next Time */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="rounded-2xl border border-zinc-800 bg-zinc-900/40 p-6 sm:p-8 backdrop-blur-md flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-zinc-800">
                <span className="font-bold text-white flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-emerald-500" />
                  Day 2+: Every Time After
                </span>
                <span className="text-xs font-mono text-zinc-500">
                  Zero Human Interruption
                </span>
              </div>

              <div className="space-y-4 text-sm font-mono">
                <div className="flex items-start gap-3">
                  <span className="text-blue-400 font-semibold shrink-0">🤖 Agent:</span>
                  <span className="text-zinc-300">
                    &quot;I need another ticket from confluence.corp.com/specs.&quot;
                  </span>
                </div>

                <div className="flex items-start gap-3">
                  <span className="text-purple-400 font-semibold shrink-0">◉ Portal:</span>
                  <span className="text-emerald-400">
                    &quot;Reused saved session. Extracted 8,400 tokens in 2.8s.&quot; ✅
                  </span>
                </div>

                <div className="flex items-start gap-3">
                  <span className="text-blue-400 font-semibold shrink-0">🤖 Agent:</span>
                  <span className="text-zinc-400">
                    &quot;...Wait, you fetched that without asking me for screenshots?&quot;
                  </span>
                </div>

                <div className="flex items-start gap-3">
                  <span className="text-purple-400 font-semibold shrink-0">◉ Portal:</span>
                  <span className="text-zinc-300">
                    &quot;That&apos;s the whole point.&quot; 😌
                  </span>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-zinc-800/60 text-xs text-zinc-500">
              Autonomous, transparent retrieval without bothering you again.
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

