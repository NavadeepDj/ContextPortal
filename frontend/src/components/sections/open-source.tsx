"use client";
import React from "react";
import { motion } from "motion/react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { GithubIcon } from "@/components/ui/icons";
import {
  Star,
  GitFork,
  Check,
  Terminal,
  ExternalLink,
  Code,
  Shield,
  Layers,
  Zap,
} from "lucide-react";

export const OpenSourceSection = () => {
  const features = [
    { label: "100% Open Source (MIT License)", desc: "Inspect every line of code" },
    { label: "Local-First Architecture", desc: "Zero cloud relays or proxies" },
    { label: "Standard Model Context Protocol", desc: "Works with Claude, Cursor, Antigravity" },
    { label: "Persistent Local Sessions", desc: "Authenticate once, reuse indefinitely" },
    { label: "Two-Tier Retrieval Engine", desc: "Fast HTTP fallback to browser" },
    { label: "Zero Credential Exposure", desc: "Session cookies never leave localhost" },
  ];

  return (
    <section className="relative py-24 sm:py-32 border-b border-zinc-900 bg-zinc-950/30 overflow-hidden">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge variant="secondary" className="mb-4">
            <Code className="h-3 w-3 mr-1 text-blue-400" />
            Open Source
          </Badge>
          <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white">
            Open source. Local-first. Built for agents.
          </h2>
          <p className="mt-4 text-zinc-400 max-w-xl mx-auto text-base sm:text-lg">
            No proprietary lock-in. No cloud subscriptions. Just reliable retrieval infrastructure.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch max-w-5xl mx-auto">
          {/* Left: 6 Trust Checkmarks */}
          <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-4">
            {features.map((feat, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 15 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: idx * 0.08 }}
                className="rounded-xl border border-zinc-800/80 bg-zinc-900/40 p-4 backdrop-blur-sm flex flex-col justify-start"
              >
                <div className="flex items-center gap-2 mb-1.5">
                  <div className="flex h-5 w-5 items-center justify-center rounded-full bg-emerald-950/80 border border-emerald-500/40 shrink-0">
                    <Check className="h-3 w-3 text-emerald-400" />
                  </div>
                  <span className="font-bold text-sm text-zinc-200">{feat.label}</span>
                </div>
                <p className="text-xs text-zinc-500 pl-7">{feat.desc}</p>
              </motion.div>
            ))}
          </div>

          {/* Right: GitHub Card */}
          <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="lg:col-span-5 rounded-2xl border border-zinc-800 bg-gradient-to-b from-zinc-900/80 to-zinc-950 p-6 flex flex-col justify-between shadow-2xl backdrop-blur-xl"
          >
            <div>
              <div className="flex items-center justify-between pb-4 border-b border-zinc-800/80 mb-4">
                <div className="flex items-center gap-2.5">
                  <div className="h-8 w-8 rounded-lg bg-zinc-800 border border-zinc-700 flex items-center justify-center">
                    <GithubIcon className="h-4.5 w-4.5 text-white" />
                  </div>
                  <div>
                    <h4 className="font-bold text-white text-sm">NavadeepDj / ContextPortal</h4>
                    <p className="text-[11px] font-mono text-zinc-500">github.com/NavadeepDj/ContextPortal</p>
                  </div>
                </div>
              </div>

              <p className="text-xs text-zinc-400 leading-relaxed">
                The authenticated fetch layer for AI agents. Bridges standard MCP clients with transparent local browser automation.
              </p>

              <div className="mt-5 flex items-center gap-4 text-xs font-mono text-zinc-400">
                <span className="flex items-center gap-1">
                  <span className="h-2 w-2 rounded-full bg-blue-500" />
                  Python 3.12+
                </span>
                <span className="flex items-center gap-1 text-zinc-500">
                  <Layers className="h-3.5 w-3.5 text-purple-400" />
                  MCP Server
                </span>
                <span className="text-emerald-400 font-semibold">v0.1.0</span>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-zinc-800/80 flex flex-col gap-2">
              <a
                href="https://github.com/NavadeepDj/ContextPortal"
                target="_blank"
                rel="noreferrer"
                className="w-full"
              >
                <Button variant="outline" className="w-full justify-center gap-2 text-xs">
                  <GithubIcon className="h-4 w-4" />
                  <span>Star on GitHub</span>
                  <ExternalLink className="h-3 w-3 text-zinc-500 ml-auto" />
                </Button>
              </a>
              <p className="text-center text-[11px] text-zinc-600 font-mono mt-1">
                Don&apos;t trust the landing page. Read the code. 😉
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};
