"use client";
import React, { useRef } from "react";
import { motion } from "motion/react";
import { Badge } from "@/ui/badge";
import { AnimatedBeam } from "@/ui/animated-beam";
import { Bot, Globe, Shield, Terminal, FileCheck, Layers } from "lucide-react";

export const TheSolutionSection = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const agentRef = useRef<HTMLDivElement>(null);
  const portalRef = useRef<HTMLDivElement>(null);
  const httpRef = useRef<HTMLDivElement>(null);
  const browserRef = useRef<HTMLDivElement>(null);
  const markdownRef = useRef<HTMLDivElement>(null);

  return (
    <section id="the-solution" className="relative py-24 sm:py-32 border-b border-zinc-900 overflow-hidden">
      {/* Background Lighting */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[550px] h-[300px] bg-blue-600/10 blur-[140px] pointer-events-none -z-10" />

      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 text-center">
        <Badge variant="glow" className="mb-4">
          The Solution
        </Badge>
        <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white">
          There&apos;s a better way.
        </h2>
        <p className="mt-4 text-zinc-400 max-w-2xl mx-auto text-base sm:text-lg">
          One request. No screenshots. No copy-paste. No site-specific API keys.
        </p>

        {/* Dynamic Architectural Beam Diagram */}
        <div
          ref={containerRef}
          className="relative mt-16 mx-auto w-full max-w-4xl rounded-2xl border border-zinc-800 bg-zinc-950/70 p-8 sm:p-12 shadow-2xl backdrop-blur-xl"
        >
          {/* Top Level: Agent */}
          <div className="flex flex-col items-center">
            <div
              ref={agentRef}
              className="z-10 flex h-14 w-14 items-center justify-center rounded-2xl border border-blue-500/40 bg-blue-950/80 shadow-lg shadow-blue-500/20"
            >
              <Bot className="h-7 w-7 text-blue-400" />
            </div>
            <span className="mt-2 text-xs font-mono font-semibold text-zinc-300">
              AI Agent (Claude / Cursor / Antigravity)
            </span>
            <span className="text-[11px] font-mono text-blue-400">
              fetch_context(&quot;https://private.site.com&quot;)
            </span>
          </div>

          {/* Middle Level: ContextPortal Gateway */}
          <div className="my-14 flex flex-col items-center">
            <div
              ref={portalRef}
              className="z-10 flex h-16 w-16 items-center justify-center rounded-2xl border-2 border-indigo-500/60 bg-gradient-to-br from-indigo-900 to-blue-950 shadow-2xl shadow-indigo-500/30"
            >
              <Shield className="h-8 w-8 text-indigo-300" />
            </div>
            <span className="mt-2 font-bold text-white text-base">
              ContextPortal Core Engine
            </span>
            <span className="text-xs text-zinc-500">
              Two-Tier Transparent Retrieval Pipeline
            </span>
          </div>

          {/* Lower Middle: Retrieval Strategies Split */}
          <div className="grid grid-cols-2 gap-8 max-w-lg mx-auto">
            {/* Tier 1: Fast HTTP */}
            <div className="flex flex-col items-center">
              <div
                ref={httpRef}
                className="z-10 flex h-12 w-12 items-center justify-center rounded-xl border border-zinc-700 bg-zinc-900/90 shadow-md"
              >
                <Globe className="h-5 w-5 text-emerald-400" />
              </div>
              <span className="mt-2 text-xs font-semibold text-zinc-300">
                Tier 1: Public HTTP
              </span>
              <span className="text-[10px] text-zinc-500 font-mono">
                httpx fast-path (~50ms)
              </span>
            </div>

            {/* Tier 2: Authenticated Session */}
            <div className="flex flex-col items-center">
              <div
                ref={browserRef}
                className="z-10 flex h-12 w-12 items-center justify-center rounded-xl border border-amber-500/40 bg-amber-950/40 shadow-md"
              >
                <Layers className="h-5 w-5 text-amber-400" />
              </div>
              <span className="mt-2 text-xs font-semibold text-zinc-300">
                Tier 2: Authenticated Browser
              </span>
              <span className="text-[10px] text-zinc-500 font-mono">
                Local Playwright Session
              </span>
            </div>
          </div>

          {/* Output Level: Clean Markdown Delivery */}
          <div className="mt-14 flex flex-col items-center">
            <div
              ref={markdownRef}
              className="z-10 flex h-14 w-14 items-center justify-center rounded-2xl border border-emerald-500/50 bg-emerald-950/80 shadow-lg shadow-emerald-500/20"
            >
              <FileCheck className="h-7 w-7 text-emerald-400" />
            </div>
            <span className="mt-2 text-xs font-mono font-semibold text-emerald-300">
              Clean, Token-Optimized Markdown
            </span>
            <span className="text-[11px] text-zinc-500">
              Returned straight to Agent context
            </span>
          </div>

          {/* Animated Connecting Beams */}
          <AnimatedBeam
            containerRef={containerRef}
            fromRef={agentRef}
            toRef={portalRef}
            duration={3}
            gradientStartColor="#3b82f6"
            gradientStopColor="#6366f1"
          />
          <AnimatedBeam
            containerRef={containerRef}
            fromRef={portalRef}
            toRef={httpRef}
            duration={4}
            delay={0.5}
            gradientStartColor="#6366f1"
            gradientStopColor="#10b981"
          />
          <AnimatedBeam
            containerRef={containerRef}
            fromRef={portalRef}
            toRef={browserRef}
            duration={4}
            delay={1}
            gradientStartColor="#6366f1"
            gradientStopColor="#f59e0b"
          />
          <AnimatedBeam
            containerRef={containerRef}
            fromRef={browserRef}
            toRef={markdownRef}
            duration={3.5}
            delay={1.5}
            gradientStartColor="#f59e0b"
            gradientStopColor="#10b981"
          />
        </div>

        {/* The Core Promises */}
        <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto text-left">
          {[
            { title: "One Request", desc: "No complex multi-turn prompting" },
            { title: "Zero Screenshots", desc: "No vision-token wastage" },
            { title: "Zero Copy-Paste", desc: "Agent reads autonomously" },
            { title: "No Custom APIs", desc: "Works with any URL in your browser" },
          ].map((item, idx) => (
            <div
              key={idx}
              className="p-4 rounded-xl border border-zinc-800/80 bg-zinc-900/40 backdrop-blur-sm"
            >
              <h4 className="text-white font-semibold text-sm">{item.title}</h4>
              <p className="text-zinc-500 text-xs mt-1">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

