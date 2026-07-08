"use client";

import { useState, useRef, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Send, User, Loader2, Mic, MicOff } from "lucide-react";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";
import { ThemeToggle } from "@/components/theme-toggle";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

// We wrap the main chat interface in a sub-component so we can use useSearchParams safely with Suspense
function ChatInterface() {
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get("q");
  
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Namaste! I am JanSevak, your AI assistant for Indian government services. How can I help you today? You can ask me about certificates, schemes, or local healthcare."
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [lang, setLang] = useState("EN");
  const scrollRef = useRef<HTMLDivElement>(null);
  const hasInitialized = useRef(false);

  // Sync Language State from Navbar
  useEffect(() => {
    const handleLangChange = () => setLang(localStorage.getItem("jansevak_lang") || "EN");
    handleLangChange();
    window.addEventListener("languageChange", handleLangChange);
    return () => window.removeEventListener("languageChange", handleLangChange);
  }, []);

  // Handle Initial Search Query from Landing Page
  useEffect(() => {
    if (initialQuery && !hasInitialized.current) {
      hasInitialized.current = true;
      sendMessage(initialQuery);
    }
  }, [initialQuery]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text.trim()
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

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    await sendMessage(input);
  };

  const toggleListening = () => {
    if (isListening) {
      setIsListening(false);
      return;
    }
    
    // Type definitions for Web Speech API
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      toast.error("Speech recognition is not supported in your browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = lang === "HI" ? "hi-IN" : "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onerror = (event: any) => {
      console.error("Speech recognition error", event.error);
      setIsListening(false);
      if (event.error !== "no-speech") {
        toast.error("Microphone error. Please try again.");
      }
    };

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setInput((prev) => prev + (prev ? " " : "") + transcript);
    };

    recognition.start();
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] max-w-4xl mx-auto relative">
      
      {/* Chat Header */}
      <div className="flex flex-col items-center justify-center pt-8 pb-6 mb-4 relative">
        <div className="absolute top-8 right-4 md:right-0">
          <ThemeToggle />
        </div>
        <h1 className="text-3xl font-bold tracking-tight mb-2">JanSevak AI</h1>
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
                    <div className="w-full h-full flex items-center justify-center bg-foreground text-background font-bold text-lg rounded-full">
                      J
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
                <div className="w-full h-full flex items-center justify-center bg-foreground text-background font-bold text-lg rounded-full">
                  J
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
              placeholder={lang === "HI" ? "योजनाओं, स्वास्थ्य देखभाल आदि के बारे में पूछें..." : "Ask about certificates, schemes, healthcare..."} 
              className="flex-1 border-0 bg-transparent shadow-none focus-visible:ring-0 text-base px-4 h-12"
              disabled={isLoading}
            />
            <Button 
              type="button" 
              size="icon" 
              variant="ghost" 
              className={`h-12 w-12 rounded-full shrink-0 transition-colors ${isListening ? 'text-red-500 bg-red-500/10 hover:bg-red-500/20 hover:text-red-600' : 'text-muted-foreground hover:text-foreground'}`} 
              onClick={toggleListening} 
              disabled={isLoading}
              title="Voice Input"
            >
              {isListening ? <MicOff className="w-5 h-5 animate-pulse" /> : <Mic className="w-5 h-5" />}
            </Button>
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
  );
}

export default function ChatPage() {
  return (
    <AppLayout role="citizen">
      <Suspense fallback={<div className="flex justify-center items-center h-[calc(100vh-8rem)]"><Loader2 className="w-8 h-8 animate-spin text-muted-foreground" /></div>}>
        <ChatInterface />
      </Suspense>
    </AppLayout>
  );
}
