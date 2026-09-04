"use client";
import React from "react";
import { motion } from "motion/react";
import { Card } from "@/ui/card";
import { Badge } from "@/ui/badge";
import { Bot, User, Camera, Upload, Copy, FileText, AlertCircle } from "lucide-react";

export const ThePainSection = () => {
  const steps = [
    {
      actor: "You",
      icon: User,
      color: "text-zinc-300",
      bg: "bg-zinc-800",
      content: '"Hey Agent, read this Jira ticket and summarize the blocker for me."',
      meta: "Task requested",
    },
    {
      actor: "Agent",
      icon: Bot,
      color: "text-blue-400",
      bg: "bg-blue-950/80 border border-blue-800/40",
      content: '"Sure thing! Fetching the webpage..."',
      meta: "Attempting fetch",
    },
    {
      actor: "Login Wall",
      icon: AlertCircle,
      color: "text-amber-400",
      bg: "bg-amber-950/40 border border-amber-800/40",
      content: "HTTP 401 Unauthorized. Please authenticate via Okta SSO.",
      meta: "Blocked",
    },
    {
      actor: "Agent gives you homework",
      icon: Bot,
      color: "text-red-400",
      bg: "bg-red-950/40 border border-red-800/40",
      content: '"Sorry, I cannot access this page. Please take screenshots of all tabs and upload them here."',
      meta: "Workflow halted",
    },
    {
      actor: "You (frustrated)",
      icon: Camera,
      color: "text-zinc-400",
      bg: "bg-zinc-900 border border-zinc-800",
      content: "Take screenshot 📸 → Crop window → Upload image → Copy comments → Paste into chat → Explain what section is which...",
      meta: "7 minutes wasted",
    },
  ];

  return (
    <section id="why" className="relative py-24 sm:py-32 border-b border-zinc-900 bg-zinc-950/40 overflow-hidden">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <Badge variant="destructive" className="mb-4">
            The Reality Today
          </Badge>
          <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white">
            Without ContextPortal
          </h2>
          <p className="mt-4 text-zinc-400 max-w-xl mx-auto text-base sm:text-lg">
            Every time your AI agent needs a protected page, you become its unpaid intern.
          </p>
        </div>

        {/* The Pain Timeline */}
        <div className="relative border-l border-zinc-800 pl-6 sm:pl-8 ml-4 sm:ml-8 space-y-8">
          {steps.map((step, idx) => {
            const Icon = step.icon;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, margin: "-80px" }}
                transition={{ duration: 0.5, delay: idx * 0.1 }}
                className="relative group"
              >
                {/* Bullet */}
                <div className="absolute -left-[35px] sm:-left-[43px] top-3.5 flex h-7 w-7 items-center justify-center rounded-full bg-zinc-900 border border-zinc-700 shadow-md">
                  <Icon className={`h-3.5 w-3.5 ${step.color}`} />
                </div>

                {/* Bubble Card */}
                <div className={`p-4 sm:p-5 rounded-xl ${step.bg} shadow-lg backdrop-blur-sm transition-transform hover:-translate-y-0.5`}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold text-sm text-white flex items-center gap-2">
                      {step.actor}
                    </span>
                    <span className="text-[11px] font-mono text-zinc-500 uppercase tracking-wider">
                      {step.meta}
                    </span>
                  </div>
                  <p className="text-sm sm:text-base text-zinc-300 font-mono">
                    {step.content}
                  </p>
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* The Punchline */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="mt-20 text-center"
        >
          <div className="inline-block rounded-2xl border border-zinc-800 bg-zinc-900/60 px-8 py-6 backdrop-blur-md shadow-2xl">
            <p className="text-xs uppercase tracking-widest text-zinc-500 font-mono mb-2">
              The honest question
            </p>
            <h3 className="text-2xl sm:text-4xl font-extrabold text-white">
              Why are we still doing this in 2026?
            </h3>
            <p className="mt-2 text-zinc-400 text-sm max-w-md mx-auto">
              Copy-pasting screenshots into an AI window is not an agent architecture.
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

