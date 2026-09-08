"use client";
import React, { useRef } from "react";
import { motion } from "motion/react";
import { Badge } from "@/components/ui/badge";
import { AnimatedBeam } from "@/components/ui/animated-beam";
import { Bot, ShieldCheck, Eye, EyeOff, Lock, FileText, Cookie } from "lucide-react";

export const PrivacySection = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const agentTopRef = useRef<HTMLDivElement>(null);
  const portalRef = useRef<HTMLDivElement>(null);
  const browserRef = useRef<HTMLDivElement>(null);
  const contextRef = useRef<HTMLDivElement>(null);

  return (
    <section id="privacy" className="relative py-24 sm:py-32 border-b border-zinc-900 overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[300px] bg-purple-600/8 blur-[120px] pointer-events-none -z-10" />

      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge variant="secondary" className="mb-4">
            <Lock className="h-3 w-3 mr-1" />
            Trust Architecture
          </Badge>
          <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white">
            Your credentials stay yours.
          </h2>
          <p className="mt-4 text-zinc-400 max-w-2xl mx-auto text-base sm:text-lg">
            ContextPortal doesn&apos;t hand your cookies, tokens, or passwords to your AI agent.
            The browser handles authentication. ContextPortal retrieves the resulting page context.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left: Animated Privacy Flow */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            ref={containerRef}
            className="relative mx-auto w-full max-w-md rounded-2xl border border-zinc-800 bg-zinc-950/80 p-8 sm:p-10 shadow-2xl backdrop-blur-xl"
          >
            {/* Agent (Top) */}
            <div className="flex flex-col items-center mb-12">
              <div
                ref={agentTopRef}
                className="z-10 flex h-14 w-14 items-center justify-center rounded-2xl border border-blue-500/40 bg-blue-950/80 shadow-lg"
              >
                <Bot className="h-7 w-7 text-blue-400" />
              </div>
              <span className="mt-2 text-xs font-mono text-zinc-300">AI Agent</span>
              <span className="text-[10px] font-mono text-blue-400/70">fetch_context(url)</span>
            </div>

            {/* ContextPortal (Middle) — with Shield */}
            <div className="flex flex-col items-center mb-12 relative">
              <div
                ref={portalRef}
                className="z-10 flex h-16 w-16 items-center justify-center rounded-2xl border-2 border-emerald-500/50 bg-gradient-to-br from-emerald-950 to-zinc-900 shadow-2xl shadow-emerald-500/20"
              >
                <ShieldCheck className="h-8 w-8 text-emerald-400" />
              </div>
              <span className="mt-2 font-bold text-white text-sm">ContextPortal</span>
              <span className="text-[10px] text-zinc-500 font-mono">Security Boundary</span>
              {/* Shield barrier visual */}
              <div className="absolute -inset-x-8 top-1/2 -translate-y-1/2 h-px bg-gradient-to-r from-transparent via-emerald-500/40 to-transparent" />
            </div>

            {/* Local Browser (Below Shield) */}
            <div className="flex flex-col items-center mb-12">
              <div
                ref={browserRef}
                className="z-10 flex h-12 w-12 items-center justify-center rounded-xl border border-amber-500/40 bg-amber-950/40 shadow-md"
              >
                <Cookie className="h-5 w-5 text-amber-400" />
              </div>
              <span className="mt-2 text-xs font-mono text-zinc-300">Your Local Browser</span>
              <span className="text-[10px] text-zinc-500">🔐 Cookies & Sessions stay here</span>
            </div>

            {/* Clean Context (Bottom) */}
            <div className="flex flex-col items-center">
              <div
                ref={contextRef}
                className="z-10 flex h-14 w-14 items-center justify-center rounded-2xl border border-emerald-500/50 bg-emerald-950/60 shadow-lg"
              >
                <FileText className="h-7 w-7 text-emerald-400" />
              </div>
              <span className="mt-2 text-xs font-mono font-semibold text-emerald-300">Clean Markdown</span>
              <span className="text-[10px] text-zinc-500">Only this reaches the Agent</span>
            </div>

            {/* Beams */}
            <AnimatedBeam containerRef={containerRef} fromRef={agentTopRef} toRef={portalRef} duration={3} gradientStartColor="#3b82f6" gradientStopColor="#10b981" />
            <AnimatedBeam containerRef={containerRef} fromRef={portalRef} toRef={browserRef} duration={4} delay={0.5} gradientStartColor="#10b981" gradientStopColor="#f59e0b" />
            <AnimatedBeam containerRef={containerRef} fromRef={browserRef} toRef={contextRef} duration={3} delay={1} gradientStartColor="#f59e0b" gradientStopColor="#10b981" reverse />
          </motion.div>

          {/* Right: Key Points */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="space-y-8"
          >
            {[
              {
                icon: EyeOff,
                color: "text-red-400",
                bg: "bg-red-950/30 border-red-800/40",
                title: "Cookies never leave your machine",
                description: "Your session cookies, tokens, and auth state remain exclusively in your local Playwright profile directory. They are never serialized, logged, or transmitted.",
              },
              {
                icon: ShieldCheck,
                color: "text-emerald-400",
                bg: "bg-emerald-950/30 border-emerald-800/40",
                title: "Agent receives sanitized Markdown only",
                description: "ContextPortal strips scripts, styles, tracking pixels, and metadata. The agent receives clean, token-optimized content — nothing more.",
              },
              {
                icon: Lock,
                color: "text-blue-400",
                bg: "bg-blue-950/30 border-blue-800/40",
                title: "No cloud. No proxy. Fully local.",
                description: "ContextPortal runs entirely on your local machine. No third-party servers, no cloud relays, no credential proxies. Your data never leaves your localhost.",
              },
            ].map((item, idx) => {
              const Icon = item.icon;
              return (
                <div key={idx} className={`rounded-xl border ${item.bg} p-5 backdrop-blur-sm`}>
                  <div className="flex items-center gap-3 mb-2">
                    <div className={`flex h-9 w-9 items-center justify-center rounded-lg bg-zinc-900/80`}>
                      <Icon className={`h-4.5 w-4.5 ${item.color}`} />
                    </div>
                    <h4 className="text-base font-bold text-white">{item.title}</h4>
                  </div>
                  <p className="text-sm text-zinc-400 leading-relaxed pl-12">
                    {item.description}
                  </p>
                </div>
              );
            })}

            <div className="pl-12 pt-2">
              <p className="text-xl font-bold text-white">
                Your browser holds the session. Your agent gets the page.<br />
                <span className="text-emerald-400">Zero cookies leaked.</span>
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};
