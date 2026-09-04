import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ContextPortal — Authenticated Web Context for AI Agents",
  description:
    "Give your AI agent a webpage. If it's protected, ContextPortal handles the messy part. Zero credentials passed to the agent. Open source, MCP-native, local-first.",
  keywords: [
    "ContextPortal",
    "MCP",
    "Model Context Protocol",
    "AI agents",
    "authenticated retrieval",
    "browser context",
    "web scraper",
  ],
  authors: [{ name: "NavadeepDj", url: "https://github.com/NavadeepDj/ContextPortal" }],
  openGraph: {
    title: "ContextPortal — Authenticated Web Context for AI Agents",
    description:
      "Your agent found the page. The page found the login wall. ContextPortal handles the rest. Stop feeding your AI screenshots.",
    url: "https://contextportal.dev",
    siteName: "ContextPortal",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "ContextPortal — Authenticated Web Context for AI Agents",
    description: "Stop feeding your AI screenshots. Give it ContextPortal.",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} dark h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-[#09090b] text-[#fafafa] font-sans selection:bg-blue-500/30 selection:text-blue-200">
        {children}
      </body>
    </html>
  );
}
