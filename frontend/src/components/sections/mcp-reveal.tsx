"use client";
import React, { useState } from "react";
import { motion } from "motion/react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { BorderBeam } from "@/components/ui/border-beam";
import { Code2, Copy, Check, Bot, FileText, Globe, Layers } from "lucide-react";

export const McpRevealSection = () => {
  const [copied, setCopied] = useState(false);

  const codeSnippet = `# MCP Tool — One semantic call
result = await fetch_context(
    "https://confluence.corp.com/display/ENG/Q3-Roadmap"
)

# Returns clean, agent-optimized Markdown
print(result.content)       # "## Q3 Engineering Roadmap\\n..."
print(result.tokens)        # 4,120
print(result.authenticated) # True
print(result.method)        # "browser"`;

  const handleCopy = () => {
    navigator.clipboard.writeText(codeSnippet);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section id="mcp" className="relative py-24 sm:py-32 border-b border-zinc-900 overflow-hidden">
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[300px] bg-indigo-600/8 blur-[140px] pointer-events-none -z-10" />

      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 text-center">
        <Badge variant="glow" className="mb-4">
          <Code2 className="h-3 w-3 mr-1" />
          Developer Experience
        </Badge>
        <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white">
          One semantic tool.<br />
          <span className="text-zinc-400">Multiple retrieval strategies underneath.</span>
        </h2>

        <div className="mt-16 grid grid-cols-1 lg:grid-cols-2 gap-8 text-left items-start">
          {/* Left: Code Block */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="relative rounded-2xl border border-zinc-800 bg-[#0c0c0f] shadow-2xl overflow-hidden"
          >
            <BorderBeam duration={15} size={300} colorFrom="#6366f1" colorTo="#3b82f6" />

            {/* Code Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-zinc-800 bg-zinc-900/50">
              <div className="flex items-center gap-1.5">
                <div className="h-2.5 w-2.5 rounded-full bg-red-500/80" />
                <div className="h-2.5 w-2.5 rounded-full bg-yellow-500/80" />
                <div className="h-2.5 w-2.5 rounded-full bg-green-500/80" />
                <span className="ml-2 text-xs font-mono text-zinc-500">
                  mcp_agent.py
                </span>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleCopy}
                className="h-7 px-2 text-xs gap-1.5"
              >
                {copied ? (
                  <>
                    <Check className="h-3 w-3 text-emerald-400" />
                    <span className="text-emerald-400">Copied</span>
                  </>
                ) : (
                  <>
                    <Copy className="h-3 w-3" />
                    <span>Copy</span>
                  </>
                )}
              </Button>
            </div>

            {/* Code Content */}
            <div className="p-5 overflow-x-auto">
              <pre className="text-sm font-mono leading-relaxed">
                <code>
                  {codeSnippet.split("\n").map((line, i) => (
                    <div key={i} className="flex">
                      <span className="w-6 shrink-0 text-right mr-4 text-zinc-700 select-none text-xs">
                        {i + 1}
                      </span>
                      <span
                        className={
                          line.startsWith("#")
                            ? "text-zinc-500"
                            : line.includes("fetch_context")
                            ? "text-blue-400"
                            : line.includes("True") || line.includes('"browser"')
                            ? "text-emerald-400"
                            : line.includes("print")
                            ? "text-purple-300"
                            : line.includes('"')
                            ? "text-amber-300"
                            : "text-zinc-300"
                        }
                      >
                        {line}
                      </span>
                    </div>
                  ))}
                </code>
              </pre>
            </div>
          </motion.div>

          {/* Right: MCP Architecture Explanation */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.15 }}
            className="space-y-6"
          >
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-6 backdrop-blur-sm">
              <h3 className="text-lg font-bold text-white mb-3">
                Model Context Protocol (MCP)
              </h3>
              <p className="text-sm text-zinc-400 leading-relaxed">
                ContextPortal exposes a single <code className="text-blue-400 bg-blue-950/40 px-1.5 py-0.5 rounded text-xs">fetch_context</code> tool
                via the <a href="https://modelcontextprotocol.io" target="_blank" rel="noreferrer" className="text-blue-400 underline underline-offset-4 hover:text-blue-300">Model Context Protocol</a> — the
                open standard for connecting AI agents to external tools. Any MCP-compatible client
                can call ContextPortal out of the box.
              </p>
            </div>

            {/* Automatic Setup Terminal Box */}
            <div className="rounded-xl border border-blue-500/30 bg-[#09090d] p-5 shadow-2xl relative overflow-hidden">
              <div className="flex items-center justify-between pb-3 mb-3 border-b border-zinc-800">
                <span className="text-xs font-mono font-bold text-blue-400 flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-blue-500 animate-pulse" />
                  Automatic Setup (Recommended)
                </span>
                <span className="text-[11px] font-mono text-zinc-500">Zero JSON editing</span>
              </div>
              <pre className="text-xs font-mono text-zinc-300 leading-relaxed overflow-x-auto">
{`$ contextportal setup

  ✓ Detected AI clients (Cursor, Antigravity, Claude)
  ✓ Injected 'context-portal' MCP configuration
  ✓ Verified local browser session storage

🎉 Ready. Now just give your agent the URL.`}
              </pre>
            </div>

            {/* Supported Clients */}
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-6 backdrop-blur-sm">
              <h4 className="text-sm font-semibold text-zinc-300 mb-4">
                Works with every MCP client
              </h4>
              <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-5 backdrop-blur-sm">
              <div className="flex items-center justify-between mb-3">
                <h4 className="text-xs font-semibold uppercase tracking-wider text-zinc-400 font-mono">
                  Supported AI Clients
                </h4>
                <span className="text-[11px] font-mono text-emerald-400">Auto + Manual</span>
              </div>
              <div className="grid grid-cols-2 gap-2.5">
                {[
                  { name: "Claude Desktop", color: "text-amber-400" },
                  { name: "Cursor", color: "text-blue-400" },
                  { name: "Google Antigravity", color: "text-purple-400" },
                  { name: "VS Code + Extensions", color: "text-emerald-400" },
                  { name: "Cursor", color: "text-blue-400", path: "Auto-detected" },
                  { name: "Google Antigravity", color: "text-purple-400", path: "Auto-detected" },
                  { name: "Claude Desktop", color: "text-amber-400", path: "Auto-detected" },
                  { name: "VS Code / Cline", color: "text-emerald-400", path: "Manual fallback" },
                ].map((client, idx) => (
                  <div
                    key={idx}
                    className="flex items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-950/60 p-2.5"
                    className="flex flex-col rounded-lg border border-zinc-800/80 bg-zinc-950/60 p-2.5"
                  >
                    <Bot className={`h-4 w-4 ${client.color}`} />
                    <span className="text-xs font-medium text-zinc-300">
                      {client.name}
                    <div className="flex items-center gap-1.5 mb-1">
                      <Bot className={`h-3.5 w-3.5 ${client.color}`} />
                      <span className="text-xs font-medium text-zinc-200">
                        {client.name}
                      </span>
                    </div>
                    <span className="text-[10px] font-mono text-zinc-500">
                      {client.path}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* MCP Config Snippet */}
            <div className="rounded-xl border border-zinc-800 bg-[#0c0c0f] p-5">
              <p className="text-xs font-mono text-zinc-500 mb-3">
                // Add to your MCP client config:
            {/* Manual Fallback Config */}
            <div className="rounded-xl border border-zinc-800/80 bg-[#0c0c0f] p-4">
              <p className="text-[11px] font-mono text-zinc-500 mb-2">
                // Manual Fallback: Standard MCP client config
              </p>
              <pre className="text-xs font-mono text-zinc-300 leading-relaxed">
              <pre className="text-[11px] font-mono text-zinc-400 leading-relaxed">
{`{
  "mcpServers": {
    "context-portal": {
      "command": "contextportal",
      "args": ["mcp"]
    }
  }
}`}
              </pre>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};
