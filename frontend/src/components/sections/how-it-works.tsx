"use client";
import React from "react";
import { motion } from "motion/react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/ui/card";
import { BorderBeam } from "@/ui/border-beam";
import { Badge } from "@/ui/badge";
import { Link2, KeyRound, FastForward } from "lucide-react";

export const HowItWorksSection = () => {
  const cards = [
    {
      step: "01",
      icon: Link2,
      title: "Connect your agent",
      description:
        "Run `contextportal setup`. It auto-detects Cursor, Antigravity, or Claude Desktop and registers the MCP server for you. Zero JSON editing.",
      tag: "Automatic Setup",
      color: "from-blue-500 to-indigo-500",
    },
    {
      step: "02",
      icon: KeyRound,
      title: "Log in once",
      description:
        "Run `contextportal login`. Log into your private sites (Jira, Confluence, SSO) in your browser once. Your session stays on your disk.",
      tag: "1-Time Human Auth",
      color: "from-indigo-500 to-purple-500",
    },
    {
      step: "03",
      icon: FastForward,
      title: "Give your agent the URL",
      description:
        "You're ready. Just paste any protected URL in your AI chat. ContextPortal retrieves the clean Markdown context autonomously.",
      tag: "Autonomous Flow",
      color: "from-purple-500 to-emerald-500",
    },
  ];

  return (
    <section className="relative py-24 sm:py-32 border-b border-zinc-900 bg-zinc-950/20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 text-center">
        <Badge variant="secondary" className="mb-4">
          Streamlined Workflow
        </Badge>
        <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white">
          How ContextPortal Works
        </h2>
        <p className="mt-4 text-zinc-400 max-w-2xl mx-auto text-base sm:text-lg">
          Install ContextPortal → Connect your agent → You&apos;re ready. <br className="hidden sm:inline" />
          <span className="text-white font-medium">Now just give your agent the URL.</span>
        </p>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
          {cards.map((card, idx) => {
            const Icon = card.icon;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.15 }}
                className="relative h-full"
              >
                <Card className="relative overflow-hidden h-full flex flex-col justify-between border-zinc-800/80 bg-zinc-950/80 p-6 sm:p-8">
                  {/* Subtle Top Glowing Border on Hover */}
                  <BorderBeam duration={12} delay={idx * 3} size={250} />

                  <div>
                    <div className="flex items-center justify-between mb-6">
                      <span className="font-mono text-3xl font-black text-zinc-700">
                        {card.step}
                      </span>
                      <div className="h-10 w-10 rounded-xl bg-zinc-900 border border-zinc-800 flex items-center justify-center">
                        <Icon className="h-5 w-5 text-blue-400" />
                      </div>
                    </div>

                    <h3 className="text-xl font-bold text-white mb-3">
                      {card.title}
                    </h3>
                    <p className="text-sm text-zinc-400 leading-relaxed">
                      {card.description}
                    </p>
                  </div>

                  <div className="mt-6 pt-4 border-t border-zinc-900">
                    <span className="text-[11px] font-mono text-zinc-500 uppercase tracking-wider">
                      {card.tag}
                    </span>
                  </div>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

