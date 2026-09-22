"use client";
import React from "react";
import { motion } from "motion/react";
import { Play, ShieldCheck, Zap, Lock, Terminal } from "lucide-react";

export const DemoVideoSection = () => {
  return (
    <section id="demo" className="relative py-20 overflow-hidden border-b border-zinc-900/80 bg-zinc-950/40">
      {/* Background glow effects */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[400px] bg-blue-600/10 blur-[150px] rounded-full pointer-events-none -z-10" />

      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 text-center">
        {/* Eyebrow */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="mb-4 inline-flex items-center gap-2"
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-3.5 py-1 text-xs font-medium text-blue-400">
            <Play className="h-3 w-3 fill-blue-400 text-blue-400" />
            <span>Watch in Action</span>
            <span className="text-zinc-600">•</span>
            <span className="text-zinc-300">Live Recording</span>
          </div>
        </motion.div>

        {/* Title */}
        <motion.h2
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white"
        >
          See ContextPortal Solve the Login Wall
        </motion.h2>

        {/* Description */}
        <motion.p
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-4 max-w-2xl mx-auto text-base sm:text-lg text-zinc-400"
        >
          Watch how an AI agent retrieves protected enterprise content in seconds — without asking for screenshots or touching your credentials.
        </motion.p>

        {/* Video Player Container with Window Frame */}
        <motion.div
          initial={{ opacity: 0, y: 25 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-10 mx-auto w-full max-w-4xl rounded-2xl border border-zinc-800 bg-zinc-950/90 shadow-2xl shadow-blue-950/30 overflow-hidden backdrop-blur-xl"
        >
          {/* Window Title Bar */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800/80 bg-zinc-900/60 text-xs font-mono text-zinc-400">
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded-full bg-red-500/80" />
              <div className="h-3 w-3 rounded-full bg-yellow-500/80" />
              <div className="h-3 w-3 rounded-full bg-green-500/80" />
              <span className="ml-2 text-zinc-400 font-sans">ContextPortal Live Demo Walkthrough</span>
            </div>
            <div className="flex items-center gap-1.5 text-[11px] text-zinc-400">
              <ShieldCheck className="h-3.5 w-3.5 text-blue-400" />
              <span>Zero-Leak Session Bridge</span>
            </div>
          </div>

          {/* Video Player */}
          <div className="relative aspect-video w-full bg-black">
            <video
              src="/demo.mp4"
              controls
              autoPlay
              loop
              muted
              playsInline
              preload="metadata"
              className="w-full h-full object-contain"
            >
              Your browser does not support the video tag.
            </video>
          </div>
        </motion.div>

        {/* 3 Step Timeline / Feature Highlights Below Video */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-4xl mx-auto text-left"
        >
          <div className="p-4 rounded-xl border border-zinc-800/80 bg-zinc-900/40">
            <div className="flex items-center gap-2 text-blue-400 text-sm font-semibold mb-1">
              <Lock className="h-4 w-4" />
              <span>1. SSO Wall Encountered</span>
            </div>
            <p className="text-xs text-zinc-400">
              The agent encounters private internal documentation behind an SSO login wall.
            </p>
          </div>

          <div className="p-4 rounded-xl border border-zinc-800/80 bg-zinc-900/40">
            <div className="flex items-center gap-2 text-indigo-400 text-sm font-semibold mb-1">
              <Terminal className="h-4 w-4" />
              <span>2. Local Session Reused</span>
            </div>
            <p className="text-xs text-zinc-400">
              ContextPortal connects via MCP to leverage your existing browser profile locally.
            </p>
          </div>

          <div className="p-4 rounded-xl border border-zinc-800/80 bg-zinc-900/40">
            <div className="flex items-center gap-2 text-emerald-400 text-sm font-semibold mb-1">
              <Zap className="h-4 w-4" />
              <span>3. Clean Markdown Delivered</span>
            </div>
            <p className="text-xs text-zinc-400">
              Clean, token-efficient Markdown is delivered in ~2.5s without leaking cookies.
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
};
