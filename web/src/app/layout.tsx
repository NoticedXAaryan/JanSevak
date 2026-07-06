import type { Metadata } from "next";
import { Inter, Outfit, Geist } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";

const geist = Geist({subsets:['latin'],variable:'--font-sans'});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "JanSevak - AI-Powered Public Services for India",
  description: "Navigate government schemes, report issues securely, and access healthcare and agricultural information instantly via WhatsApp and Telegram.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={cn("h-full", "antialiased", inter.variable, outfit.variable, "font-sans", geist.variable)}
    >
      <body className="min-h-full flex flex-col font-sans bg-background text-foreground relative">
        <div className="fixed top-0 left-0 right-0 h-1 z-[9999] bg-gradient-to-r from-[#FF9933] via-white to-[#138808]"></div>
        {children}
      </body>
    </html>
  );
}
