"use client";

import { Button, buttonVariants } from "@/components/ui/button";
import { ArrowRight, Bot, ShieldAlert, FileText, Globe2, Fingerprint, Lock, Zap, Building2, CheckCircle2 } from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import React, { useRef } from "react";
import { motion } from "framer-motion";

// 21st.dev Components
import { BackgroundGradientAnimation } from "@/components/ui/background-gradient-animation";
import { TextShimmer } from "@/components/ui/text-shimmer";
import { BentoGrid, BentoGridItem } from "@/components/ui/bento-grid";
import { AnimatedCounter } from "@/components/ui/animated-counter";
import { Marquee } from "@/components/ui/marquee";
import { DotPattern } from "@/components/ui/dot-pattern";
import { AnimatedBeam } from "@/components/ui/animated-beam";

export default function LandingPage() {
  return (
    <div className="bg-background min-h-screen overflow-x-hidden">
      {/* 1. HERO SECTION */}
      <section className="relative w-full h-[90vh] min-h-[600px] flex items-center justify-center">
        <div className="absolute inset-0 z-0 overflow-hidden bg-background">
          {/* Subtle Tricolor Orbs (Indian Motif) */}
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-orange-500/10 rounded-full blur-[128px] animate-[float_20s_ease-in-out_infinite]" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[40rem] h-[40rem] bg-white/5 rounded-full blur-[128px] animate-[float_25s_ease-in-out_infinite_reverse]" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-green-500/10 rounded-full blur-[128px] animate-[float_22s_ease-in-out_infinite_1s]" />
          <div className="absolute inset-0 bg-[url('/noise.svg')] opacity-[0.015] mix-blend-overlay" />
        </div>
        
        <div className="relative z-10 px-4 flex flex-col items-center justify-center text-center">
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            <h1 className="text-5xl md:text-7xl lg:text-8xl font-heading font-bold tracking-tight mb-6 max-w-4xl drop-shadow-2xl">
              AI-Powered Public Services for <br className="hidden md:block" />
              <TextShimmer duration={2.5} className="text-transparent bg-clip-text bg-[linear-gradient(110deg,#FF9933,45%,#fff,55%,#138808)] inline-block mt-2">
                India
              </TextShimmer>
            </h1>
          </motion.div>
          
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="text-xl md:text-2xl text-muted-foreground mb-12 max-w-3xl leading-relaxed drop-shadow-md font-medium"
          >
            Navigate schemes, report issues securely, and access healthcare information instantly. JanSevak bridges the gap between citizens and the government.
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.8 }}
            className="flex flex-col sm:flex-row gap-6"
          >
            <Link href="/chat" className={cn(buttonVariants({ size: "lg" }), "group relative overflow-hidden px-8 py-6 text-lg rounded-full bg-foreground text-background shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1")}>
              <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-emerald-500/20 via-orange-500/20 to-emerald-500/20 opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-xl"></div>
              <Bot className="mr-2 w-5 h-5 group-hover:animate-bounce relative z-10" /> 
              <span className="relative z-10 font-bold">Ask JanSevak AI</span>
            </Link>
            <Link href="/services" className={cn(buttonVariants({ variant: "outline", size: "lg" }), "group px-8 py-6 text-lg rounded-full liquid-glass text-foreground hover:bg-foreground/5 transition-all duration-300 border-border hover:-translate-y-1")}>
              <span className="font-medium">Explore Services</span> 
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* 2. FEATURES SECTION (Bento Grid) */}
      <section className="px-4 py-32 bg-background relative border-y border-border">
        <DotPattern className="opacity-40 dark:opacity-20 text-border" />
        <div className="max-w-7xl mx-auto relative z-10">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-heading font-bold mb-4 tracking-tight">Empowering Citizens</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto text-lg">One unified platform replacing fragmented government portals.</p>
          </div>
          
          <BentoGrid className="max-w-5xl mx-auto">
            <BentoGridItem
              title="Multi-lingual AI Chat"
              description="Chat in your native language. JanSevak translates complex bureaucratic jargon into simple terms instantly, supporting 22+ official Indian languages."
              header={<div className="flex flex-1 w-full h-full min-h-[6rem] rounded-xl bg-gradient-to-br from-border/50 to-background dark:to-background border border-transparent dark:border-white/[0.1] [mask-image:linear-gradient(to_bottom,white,transparent)] flex-col items-center justify-center"><Bot className="w-16 h-16 text-foreground opacity-50" /></div>}
              icon={<Globe2 className="h-5 w-5 text-foreground" />}
              className="md:col-span-2 liquid-glass hover:-translate-y-1"
            />
            <BentoGridItem
              title="Secure Whistleblowing"
              description="Submit corruption reports via cryptographically sealed envelopes."
              header={<div className="flex flex-1 w-full h-full min-h-[6rem] rounded-xl bg-gradient-to-br from-border/50 to-background dark:to-background border border-transparent dark:border-white/[0.1] [mask-image:linear-gradient(to_bottom,white,transparent)] flex-col items-center justify-center"><ShieldAlert className="w-12 h-12 text-foreground opacity-50" /></div>}
              icon={<Lock className="h-5 w-5 text-foreground" />}
              className="md:col-span-1 liquid-glass hover:-translate-y-1"
            />
            <BentoGridItem
              title="Smart Schemes"
              description="Our eligibility engine automatically matches your profile against thousands of central and state subsidies."
              header={<div className="flex flex-1 w-full h-full min-h-[6rem] rounded-xl bg-gradient-to-br from-border/50 to-background dark:to-background border border-transparent dark:border-white/[0.1] [mask-image:linear-gradient(to_bottom,white,transparent)] flex-col items-center justify-center"><FileText className="w-12 h-12 text-foreground opacity-50" /></div>}
              icon={<Zap className="h-5 w-5 text-foreground" />}
              className="md:col-span-1 liquid-glass hover:-translate-y-1"
            />
            <BentoGridItem
              title="DigiLocker Integrated"
              description="Fetch, verify, and attach your official documents instantly with zero manual uploads."
              header={<div className="flex flex-1 w-full h-full min-h-[6rem] rounded-xl bg-gradient-to-br from-border/50 to-background dark:to-background border border-transparent dark:border-white/[0.1] [mask-image:linear-gradient(to_bottom,white,transparent)] flex-col items-center justify-center"><Fingerprint className="w-16 h-16 text-foreground opacity-50" /></div>}
              icon={<CheckCircle2 className="h-5 w-5 text-foreground" />}
              className="md:col-span-2 liquid-glass hover:-translate-y-1"
            />
          </BentoGrid>
        </div>
      </section>

      {/* 3. HOW IT WORKS (Animated Beam) */}
      <section className="px-4 py-32 bg-background relative overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-heading font-bold mb-4 tracking-tight">How JanSevak Works</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto text-lg">A seamless pipeline from your request to department resolution.</p>
          </div>
          
          <BeamDemo />
        </div>
      </section>

      {/* 4. STATS SECTION (Animated Counter) */}
      <section className="px-4 py-24 bg-background relative border-y border-border">
        <DotPattern className="opacity-40 dark:opacity-20 text-border" />
        <div className="max-w-5xl mx-auto relative z-10 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div className="flex flex-col items-center space-y-2 p-6 rounded-2xl liquid-glass">
            <div className="text-4xl md:text-5xl font-bold text-foreground flex items-center">
              <AnimatedCounter value={10} direction="up" />M+
            </div>
            <div className="text-sm text-muted-foreground font-medium">Queries Answered</div>
          </div>
          <div className="flex flex-col items-center space-y-2 p-6 rounded-2xl liquid-glass">
            <div className="text-4xl md:text-5xl font-bold text-foreground flex items-center">
              <AnimatedCounter value={500} direction="up" />+
            </div>
            <div className="text-sm text-muted-foreground font-medium">Schemes Indexed</div>
          </div>
          <div className="flex flex-col items-center space-y-2 p-6 rounded-2xl liquid-glass">
            <div className="text-4xl md:text-5xl font-bold text-foreground flex items-center">
              <AnimatedCounter value={48} direction="up" />h
            </div>
            <div className="text-sm text-muted-foreground font-medium">Avg Resolution Time</div>
          </div>
          <div className="flex flex-col items-center space-y-2 p-6 rounded-2xl liquid-glass">
            <div className="text-4xl md:text-5xl font-bold text-foreground flex items-center">
              <AnimatedCounter value={22} direction="up" />
            </div>
            <div className="text-sm text-muted-foreground font-medium">Languages Supported</div>
          </div>
        </div>
      </section>

      {/* 5. TESTIMONIALS (Marquee) */}
      <section className="px-4 py-32 bg-background relative overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-heading font-bold mb-4 tracking-tight">Voices of the Nation</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto text-lg">Real impact stories from citizens across India.</p>
          </div>
          
          <div className="relative flex w-full flex-col items-center justify-center overflow-hidden">
            <Marquee pauseOnHover className="[--duration:20s]">
              {reviews.map((review) => (
                <ReviewCard key={review.username} {...review} />
              ))}
            </Marquee>
            <Marquee reverse pauseOnHover className="[--duration:25s]">
              {reviews.map((review) => (
                <ReviewCard key={review.username} {...review} />
              ))}
            </Marquee>
            <div className="pointer-events-none absolute inset-y-0 left-0 w-1/3 bg-gradient-to-r from-background dark:from-background"></div>
            <div className="pointer-events-none absolute inset-y-0 right-0 w-1/3 bg-gradient-to-l from-background dark:from-background"></div>
          </div>
        </div>
      </section>
      
      {/* 6. CTA */}
      <section className="px-4 py-24 bg-background text-center border-t border-border">
        <h2 className="text-3xl md:text-4xl font-heading font-bold mb-6">Ready to simplify your public services?</h2>
        <p className="text-muted-foreground mb-8 max-w-lg mx-auto">Join millions of Indians who are already using JanSevak to interact with the government effortlessly.</p>
        <Link href="/chat" className={cn(buttonVariants({ size: "lg" }), "px-8 py-6 text-lg rounded-full bg-foreground text-background hover:bg-foreground/90 shadow-xl transition-all hover:scale-105")}>
          Start Chatting Now
        </Link>
      </section>
    </div>
  );
}

// --- Helper Components for Demo ---

function BeamDemo() {
  const containerRef = useRef<HTMLDivElement>(null);
  const citizenRef = useRef<HTMLDivElement>(null);
  const aiRef = useRef<HTMLDivElement>(null);
  const deptRef = useRef<HTMLDivElement>(null);

  return (
    <div
      className="relative flex h-[400px] w-full max-w-4xl mx-auto items-center justify-center overflow-hidden rounded-2xl border border-border bg-background p-10 md:shadow-xl liquid-glass"
      ref={containerRef}
    >
      <div className="flex h-full w-full flex-col items-stretch justify-between gap-10">
        <div className="flex flex-row justify-between items-center h-full">
          <div
            ref={citizenRef}
            className="z-10 flex h-24 w-24 flex-col items-center justify-center rounded-full border border-border bg-background shadow-sm liquid-glass"
          >
            <Globe2 className="h-10 w-10 text-foreground" />
            <span className="text-xs font-medium mt-1">Citizen</span>
          </div>
          <div
            ref={aiRef}
            className="z-10 flex h-32 w-32 flex-col items-center justify-center rounded-full border border-border bg-background shadow-[0_0_30px_rgba(255,153,51,0.15)] liquid-glass"
          >
            <Bot className="h-14 w-14 text-foreground" />
            <span className="text-sm font-bold text-foreground mt-1">JanSevak AI</span>
          </div>
          <div
            ref={deptRef}
            className="z-10 flex h-24 w-24 flex-col items-center justify-center rounded-full border border-border bg-background shadow-sm liquid-glass"
          >
            <Building2 className="h-10 w-10 text-foreground" />
            <span className="text-xs font-medium mt-1">Department</span>
          </div>
        </div>
      </div>

      <AnimatedBeam
        containerRef={containerRef}
        fromRef={citizenRef}
        toRef={aiRef}
        curvature={-50}
        endYOffset={-10}
      />
      <AnimatedBeam
        containerRef={containerRef}
        fromRef={aiRef}
        toRef={deptRef}
        curvature={50}
        startYOffset={10}
      />
    </div>
  );
}

const reviews = [
  {
    name: "Ramesh Kumar",
    username: "@ramesh_k",
    body: "JanSevak helped me find the PM KISAN scheme in Hindi. The AI chat was so easy to use, I got registered in 10 minutes.",
    img: "https://api.dicebear.com/7.x/avataaars/svg?seed=Ramesh",
  },
  {
    name: "Priya Sharma",
    username: "@priya_s",
    body: "I used the secure whistleblowing feature to report a local issue. The anonymity gave me peace of mind, and action was taken fast.",
    img: "https://api.dicebear.com/7.x/avataaars/svg?seed=Priya",
  },
  {
    name: "Dr. Ananya Singh",
    username: "@ananya_doc",
    body: "As a doctor, verifying patient PMJAY eligibility used to take hours. Now I just use JanSevak on my phone.",
    img: "https://api.dicebear.com/7.x/avataaars/svg?seed=Ananya",
  },
  {
    name: "Vikram Patil",
    username: "@vikram_p",
    body: "The Marathi language support is incredible. My elderly father can now check his pension status by himself.",
    img: "https://api.dicebear.com/7.x/avataaars/svg?seed=Vikram",
  },
  {
    name: "Sunita Devi",
    username: "@sunita_d",
    body: "I didn't know I was eligible for the Ujjwala Yojana until JanSevak suggested it to me based on my profile.",
    img: "https://api.dicebear.com/7.x/avataaars/svg?seed=Sunita",
  },
];

const ReviewCard = ({
  img,
  name,
  username,
  body,
}: {
  img: string;
  name: string;
  username: string;
  body: string;
}) => {
  return (
    <figure
      className={cn(
        "relative w-72 cursor-pointer overflow-hidden rounded-xl p-6 mx-4 liquid-glass",
        "border-border hover:bg-accent/50",
      )}
    >
      <div className="flex flex-row items-center gap-3">
        <img className="rounded-full" width="40" height="40" alt="" src={img} />
        <div className="flex flex-col">
          <figcaption className="text-sm font-medium dark:text-white">
            {name}
          </figcaption>
          <p className="text-xs font-medium dark:text-white/40">{username}</p>
        </div>
      </div>
      <blockquote className="mt-4 text-sm leading-relaxed text-muted-foreground">{body}</blockquote>
    </figure>
  );
};
