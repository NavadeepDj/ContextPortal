"use client";
import React, { useState } from "react";
import { motion } from "motion/react";
import { Button } from "@/components/ui/button";
import { ShimmerButton } from "@/components/ui/shimmer-button";
import { GithubIcon } from "@/components/ui/icons";
import { Terminal, Copy, Check, ExternalLink, Sparkles } from "lucide-react";

export const FinalCtaSection = () => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const installCmd = "uv tool install contextportal";
  const pipCmd = "pip install contextportal";

  const handleCopy = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <section id="install" className="relative py-28 sm:py-36 overflow-hidden">
      {/* Glow highlight */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[350px] bg-gradient-to-r from-blue-600/15 via-indigo-600/10 to-purple-600/15 blur-[150px] pointer-events-none -z-10" />

      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 text-center flex flex-col items-center">
        {/* Headline */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-3 py-1 text-xs font-medium text-blue-400 mb-6 backdrop-blur-sm">
            <Sparkles className="h-3.5 w-3.5" />
            <span>Ready in under 2 minutes</span>
          </div>

          <h2 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight">
            Stop feeding your AI screenshots. <br />
            <span className="bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
              Authenticate once. Read continuously.
            </span>
          </h2>

          <p className="mt-6 text-lg sm:text-xl text-zinc-400 max-w-2xl mx-auto leading-relaxed">
            Give your agent a retrieval tool, not a browser to operate. Install ContextPortal in under 2 minutes.
          </p>
        </motion.div>

        {/* Command Box */}
        <motion.div
          initial={{ opacity: 0, scale: 0.96 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="mt-10 w-full max-w-xl flex flex-col gap-3"
        >
          {/* Primary uv tool install */}
          <div className="flex items-center justify-between rounded-xl border border-zinc-800 bg-[#09090c] p-3.5 sm:p-4 shadow-xl">
            <div className="flex items-center gap-3 font-mono text-sm sm:text-base text-zinc-200">
              <span className="text-zinc-600 select-none">$</span>
              <span>{installCmd}</span>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => handleCopy(installCmd, 0)}
              className="h-8 px-3 text-xs gap-1.5 text-zinc-400 hover:text-white"
            >
              {copiedIndex === 0 ? (
                <>
                  <Check className="h-3.5 w-3.5 text-emerald-400" />
                  <span className="text-emerald-400">Copied</span>
                </>
              ) : (
                <>
                  <Copy className="h-3.5 w-3.5" />
                  <span>Copy</span>
                </>
              )}
            </Button>
          </div>

          {/* Fallback pip install */}
          <div className="flex items-center justify-between rounded-xl border border-zinc-900 bg-[#09090c]/60 p-2.5 sm:p-3 text-xs">
            <div className="flex items-center gap-2 font-mono text-zinc-400">
              <span className="text-zinc-700 select-none">$</span>
              <span>{pipCmd}</span>
            </div>
            <button
              onClick={() => handleCopy(pipCmd, 1)}
              className="text-zinc-500 hover:text-zinc-300 font-mono text-[11px] px-2 py-1 rounded"
            >
              {copiedIndex === 1 ? "Copied!" : "Copy"}
            </button>
          </div>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="mt-10 flex flex-wrap items-center justify-center gap-4"
        >
          <a
            href="https://pypi.org/project/contextportal/"
            target="_blank"
            rel="noreferrer"
          >
            <ShimmerButton
              shimmerColor="#60a5fa"
              className="font-medium text-sm gap-2 px-8 py-4 shadow-blue-500/25"
            >
              <Terminal className="h-4 w-4 text-blue-400" />
              <span>Get ContextPortal on PyPI</span>
            </ShimmerButton>
          </a>
          <a
            href="https://github.com/NavadeepDj/ContextPortal"
            target="_blank"
            rel="noreferrer"
          >
            <Button variant="outline" size="lg" className="gap-2">
              <GithubIcon className="h-4 w-4" />
              <span>Star on GitHub</span>
              <ExternalLink className="h-4 w-4 text-zinc-500" />
            </Button>
          </a>
        </motion.div>

        {/* Closing Tagline */}
        <p className="mt-16 font-mono text-xs sm:text-sm text-zinc-400 uppercase tracking-widest text-center">
          Authenticate once. Retrieve context continuously. Zero cookies leaked.
        </p>
      </div>
    </section>
  );
};
