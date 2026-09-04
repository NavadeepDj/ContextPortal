"use client";
import React, { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Button } from "@/ui/button";
import { Badge } from "@/ui/badge";
import { ShimmerButton } from "@/ui/shimmer-button";
import { Spotlight } from "@/ui/spotlight";
import { Particles } from "@/ui/particles";
import {
  Lock,
  ArrowRight,
  Terminal,
  ExternalLink,
  Bot,
  Sparkles,
  CheckCircle2,
  Globe,
  FileCode,
  ShieldCheck,
} from "lucide-react";

export const HeroSection = () => {
  const [demoUrl, setDemoUrl] = useState("https://jira.internal.company.com/browse/ENG-4291");
  const [fetchingState, setFetchingState] = useState<"idle" | "fetching" | "success">("idle");
  const [fetchLog, setFetchLog] = useState<string[]>([]);

  const handleSimulateFetch = () => {
    if (fetchingState === "fetching") return;
    setFetchingState("fetching");
    setFetchLog([]);

    const steps = [
      "Target URL: " + demoUrl,
      "Step 1: Attempting public HTTP tier...",
      "HTTP Status 403 Forbidden: SSO wall detected (Atlassian Cloud).",
      "Step 2: Transparent escalation to local Playwright session...",
      "Loaded stored session from ~/.contextportal/playwright_profile",
      "Executing background DOM extraction (Readability engine)...",
      "Synthesizing clean, LLM-ready ATX Markdown...",
      "Success: 4,120 tokens ready. 0 cookies exposed.",
    ];

    steps.forEach((step, i) => {
      setTimeout(() => {
        setFetchLog((prev) => [...prev, step]);
        if (i === steps.length - 1) {
          setFetchingState("success");
        }
      }, (i + 1) * 450);
    });
  };

  return (
    <section className="relative min-h-[92vh] flex flex-col items-center justify-center pt-20 pb-24 overflow-hidden border-b border-zinc-900/60">
      {/* Background Ambience */}
      <Spotlight className="-top-40 left-0 md:left-48 md:-top-20" />
      <Particles className="absolute inset-0 -z-10" quantity={40} />
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-blue-600/10 blur-[130px] rounded-full pointer-events-none -z-10" />

      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 text-center flex flex-col items-center">
        {/* Top Eyebrow Tag */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-6 flex items-center gap-2"
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-3 py-1 text-xs font-medium text-blue-400 backdrop-blur-sm">
            <Sparkles className="h-3.5 w-3.5 text-blue-400" />
            <span>Introducing ContextPortal v0.1.0</span>
            <span className="text-zinc-600">•</span>
            <span className="text-zinc-300">PyPI Release</span>
          </div>
        </motion.div>

        {/* The Punchy Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-tight text-white max-w-4xl leading-[1.08]"
        >
          Your agent found the page. <br />
          <span className="bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
            The page found the login wall.
          </span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-6 max-w-2xl text-lg sm:text-xl text-zinc-400 leading-relaxed"
        >
          Give your AI agent a webpage. If it&apos;s protected, ContextPortal handles
          the messy authentication part.{" "}
          <span className="text-zinc-200 font-medium">
            Log in once in your browser. Let your agent read forever.
          </span>
        </motion.p>

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-8 flex flex-wrap items-center justify-center gap-4"
        >
          <a href="#install">
            <ShimmerButton
              shimmerColor="#60a5fa"
              className="font-medium text-sm gap-2 px-6 py-3.5 shadow-blue-500/20"
            >
              <Terminal className="h-4 w-4 text-blue-400" />
              <span>uv tool install contextportal</span>
            </ShimmerButton>
          </a>
          <a
            href="https://github.com/NavadeepDj/ContextPortal"
            target="_blank"
            rel="noreferrer"
          >
            <Button variant="outline" size="lg" className="gap-2">
              <span>View Source on GitHub</span>
              <ExternalLink className="h-4 w-4 text-zinc-500" />
            </Button>
          </a>
        </motion.div>

        {/* Interactive Hero Simulator */}
        <motion.div
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.4 }}
          className="mt-14 w-full max-w-3xl rounded-2xl border border-zinc-800 bg-zinc-950/80 p-3 sm:p-5 shadow-2xl backdrop-blur-xl"
        >
          {/* Mock Browser Header */}
          <div className="flex items-center justify-between pb-3 border-b border-zinc-900 text-xs text-zinc-500 font-mono">
            <div className="flex items-center gap-1.5">
              <div className="h-2.5 w-2.5 rounded-full bg-red-500/80" />
              <div className="h-2.5 w-2.5 rounded-full bg-yellow-500/80" />
              <div className="h-2.5 w-2.5 rounded-full bg-green-500/80" />
              <span className="ml-2 text-zinc-500">contextportal mcp-interactive-demo</span>
            </div>
            <div className="flex items-center gap-1 text-[11px] text-zinc-400">
              <ShieldCheck className="h-3.5 w-3.5 text-blue-400" />
              <span>Authenticated Proxy Active</span>
            </div>
          </div>

          {/* Interactive URL Input Bar */}
          <div className="mt-3.5 flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
            <div className="relative flex-1">
              <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none text-zinc-500">
                <Lock className="h-4 w-4 text-amber-400" />
              </div>
              <input
                type="text"
                value={demoUrl}
                onChange={(e) => setDemoUrl(e.target.value)}
                placeholder="Enter any protected URL..."
                className="w-full pl-9 pr-3 py-2.5 rounded-lg border border-zinc-800 bg-zinc-900/90 text-sm font-mono text-zinc-200 focus:outline-none focus:border-blue-500/70 transition-colors"
              />
            </div>
            <Button
              onClick={handleSimulateFetch}
              disabled={fetchingState === "fetching"}
              variant="glow"
              className="sm:w-auto w-full px-5 text-sm gap-2"
            >
              {fetchingState === "fetching" ? (
                <>
                  <div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  <span>Fetching...</span>
                </>
              ) : (
                <>
                  <span>Simulate Fetch</span>
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </Button>
          </div>

          {/* Real-time Fetch Output Terminal */}
          <div className="mt-4 rounded-lg bg-[#050507] border border-zinc-900 p-4 text-left font-mono text-xs text-zinc-300 min-h-[160px] flex flex-col justify-start overflow-hidden">
            {fetchLog.length === 0 ? (
              <div className="flex flex-col items-center justify-center my-auto py-6 text-zinc-500">
                <Bot className="h-7 w-7 text-zinc-600 mb-2" />
                <p>Click &quot;Simulate Fetch&quot; to test how ContextPortal rescues your AI agent.</p>
              </div>
            ) : (
              <div className="space-y-1.5 overflow-y-auto max-h-48">
                {fetchLog.map((log, index) => (
                  <div key={index} className="flex items-start gap-2">
                    <span className="text-zinc-600 select-none">&gt;</span>
                    <span
                      className={
                        log.includes("Success")
                          ? "text-green-400 font-semibold"
                          : log.includes("403")
                          ? "text-amber-400"
                          : log.includes("Playwright")
                          ? "text-blue-400"
                          : "text-zinc-300"
                      }
                    >
                      {log}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </motion.div>

        {/* Narrative Emoji Pipeline */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="mt-10 flex flex-wrap items-center justify-center gap-3 text-xs sm:text-sm font-mono text-zinc-500 select-none"
        >
          <span className="flex items-center gap-1 text-zinc-400">🤖 Agent</span>
          <span>→</span>
          <span className="flex items-center gap-1 text-blue-400">🔗 Private URL</span>
          <span>→</span>
          <span className="flex items-center gap-1 text-amber-400">🔒 Login Wall</span>
          <span>→</span>
          <span className="flex items-center gap-1 text-purple-400">◉ ContextPortal</span>
          <span>→</span>
          <span className="flex items-center gap-1 text-emerald-400">📄 Clean Markdown</span>
          <span>→</span>
          <span className="flex items-center gap-1 text-zinc-400">🤖 Agent</span>
        </motion.div>
      </div>
    </section>
  );
};

