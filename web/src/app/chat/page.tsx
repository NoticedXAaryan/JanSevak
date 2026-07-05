"use client";

import { useState, useRef, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Send, User, Loader2 } from "lucide-react";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";
import Image from "next/image";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Namaste! I am JanSevak, your AI assistant for Indian government services. How can I help you today? You can ask me about certificates, schemes, or local healthcare."
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // In a real app, this connects to our FastAPI backend: /api/v1/chat
      const res = await fetch("http://localhost:8000/api/v1/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage.content, session_id: "demo_user" })
      });

      if (!res.ok) {
        throw new Error("Failed to connect to AI Server");
      }

      const data = await res.json();
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response || "I received your query, but there was an error processing the response."
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      toast.error("Failed to reach AI. Using fallback response.");
      
      setTimeout(() => {
        setMessages(prev => [...prev, {
          id: (Date.now() + 1).toString(),
          role: "assistant",
          content: "I am having trouble connecting to the government database right now. Please try again later or contact your local Seva Kendra."
        }]);
        setIsLoading(false);
      }, 1000);
      return;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AppLayout role="citizen">
      <div className="flex flex-col h-[calc(100vh-8rem)] max-w-4xl mx-auto relative">
        
        {/* Chat Header */}
        <div className="flex flex-col items-center justify-center pt-8 pb-6 mb-4">
          <div className="relative w-16 h-16 rounded-2xl bg-foreground flex items-center justify-center shadow-2xl mb-4 overflow-hidden border border-border">
            <Image src="/jansevak-logo.png" alt="JanSevak Logo" fill className="object-cover" />
            <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-emerald-500 rounded-full border-2 border-background animate-pulse z-10"></div>
          </div>
          <h1 className="text-2xl font-bold tracking-tight">JanSevak AI</h1>
          <p className="text-sm text-muted-foreground">Your personal assistant for government services</p>
        </div>

        {/* Messages Area */}
        <ScrollArea className="flex-1 px-4 md:px-8 mb-24">
          <div className="space-y-6 pb-12 flex flex-col">
            <AnimatePresence initial={false}>
              {messages.map((msg) => (
                <motion.div 
                  key={msg.id}
                  initial={{ opacity: 0, y: 10, scale: 0.98 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ duration: 0.3, ease: "easeOut" }}
                  className={`flex gap-4 max-w-[85%] ${msg.role === "user" ? "self-end flex-row-reverse" : "self-start"}`}
                >
                  <Avatar className="h-10 w-10 shrink-0 shadow-md">
                    {msg.role === "assistant" ? (
                      <div className="w-full h-full bg-foreground flex items-center justify-center relative overflow-hidden border border-border">
                        <Image src="/jansevak-logo.png" alt="JanSevak Logo" fill className="object-cover" />
                      </div>
                    ) : (
                      <AvatarFallback className="bg-muted text-muted-foreground"><User className="w-5 h-5" /></AvatarFallback>
                    )}
                  </Avatar>
                  
                  <div className={`rounded-2xl px-5 py-4 shadow-sm ${
                    msg.role === "user" 
                      ? "bg-foreground text-background" 
                      : "liquid-glass relative overflow-hidden"
                  }`}>
                    {msg.role === "assistant" && (
                      <div className="absolute top-0 left-0 w-full h-[2px] tricolor-glow"></div>
                    )}
                    <p className="text-[15px] leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            
            {isLoading && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex gap-4 self-start max-w-[85%]"
              >
                <Avatar className="h-10 w-10 shrink-0 shadow-md">
                  <div className="w-full h-full bg-foreground flex items-center justify-center relative overflow-hidden border border-border">
                    <Image src="/jansevak-logo.png" alt="JanSevak Logo" fill className="object-cover" />
                  </div>
                </Avatar>
                <div className="rounded-2xl px-5 py-4 liquid-glass flex items-center gap-3">
                  <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
                  <span className="text-sm text-muted-foreground">JanSevak is thinking...</span>
                </div>
              </motion.div>
            )}
            <div ref={scrollRef} className="h-4" />
          </div>
        </ScrollArea>

        {/* Floating Input Area */}
        <div className="absolute bottom-4 left-0 right-0 px-4">
          <div className="max-w-3xl mx-auto liquid-glass rounded-full p-2 shadow-2xl relative">
            <div className="absolute -top-px -left-px -right-px h-px tricolor-glow rounded-t-full opacity-50"></div>
            <form onSubmit={handleSend} className="flex gap-2 items-center">
              <Input 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about certificates, schemes, healthcare..." 
                className="flex-1 border-0 bg-transparent shadow-none focus-visible:ring-0 text-base px-4 h-12"
                disabled={isLoading}
              />
              <Button type="submit" size="icon" className="h-12 w-12 rounded-full shrink-0 shadow-md" disabled={isLoading || !input.trim()}>
                <Send className="w-5 h-5 ml-1" />
              </Button>
            </form>
          </div>
          <p className="text-center text-xs text-muted-foreground mt-3">
            JanSevak AI can make mistakes. Always verify critical information at official portals.
          </p>
        </div>
        
      </div>
    </AppLayout>
  );
}
