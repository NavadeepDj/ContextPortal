import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { HeroSection } from "@/components/sections/hero";
import { ThePainSection } from "@/components/sections/the-pain";
import { TheSolutionSection } from "@/components/sections/the-solution";
import { HowItWorksSection } from "@/components/sections/how-it-works";
import { DialogueSection } from "@/components/sections/dialogue";
import { PrivacySection } from "@/components/sections/privacy";
import { NotABrowserSection } from "@/components/sections/not-a-browser";
import { McpRevealSection } from "@/components/sections/mcp-reveal";
import { OpenSourceSection } from "@/components/sections/open-source";
import { FinalCtaSection } from "@/components/sections/final-cta";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-[#09090b] text-[#fafafa]">
      <Navbar />
      <main className="flex-1 flex flex-col">
        <HeroSection />
        <ThePainSection />
        <TheSolutionSection />
        <HowItWorksSection />
        <DialogueSection />
        <PrivacySection />
        <NotABrowserSection />
        <McpRevealSection />
        <OpenSourceSection />
        <FinalCtaSection />
      </main>
      <Footer />
    </div>
  );
}
