"use client";

import { useState, useRef, useEffect } from "react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Send, User, Bot, Loader2 } from "lucide-react";
import { toast } from "sonner";

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
      // For demo purposes if backend isn't running, we mock a delay
      const res = await fetch("http://localhost:8000/api/v1/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage.content, session_id: "demo_user" })
      });

      if (!res.ok) {
        throw new Error("Failed to connect to AI Server");
      }

      // Handle streaming or JSON response
      const data = await res.json();
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response || "I received your query, but there was an error processing the response."
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      toast.error("Failed to reach AI. Using fallback response.");
      
      // Fallback for demo when DB/Backend is down
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
      <div className="flex flex-col h-[calc(100vh-8rem)] max-w-4xl mx-auto border rounded-xl bg-background shadow-sm overflow-hidden">
        {/* Chat Header */}
        <div className="flex items-center p-4 border-b bg-card">
          <Avatar className="h-10 w-10 border mr-3">
            <AvatarImage src="/janseva-logo.png" />
            <AvatarFallback className="bg-primary/10 text-primary"><Bot className="w-5 h-5" /></AvatarFallback>
          </Avatar>
          <div>
            <h2 className="font-semibold text-lg leading-tight">JanSevak AI</h2>
            <p className="text-xs text-muted-foreground flex items-center">
              <span className="w-2 h-2 rounded-full bg-emerald-500 mr-1.5 animate-pulse"></span>
              Online and ready to assist
            </p>
          </div>
        </div>

        {/* Messages Area */}
        <ScrollArea className="flex-1 p-4">
          <div className="space-y-4 pb-4">
            {messages.map((msg) => (
              <div 
                key={msg.id} 
                className={`flex gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}
              >
                <Avatar className="h-8 w-8 shrink-0">
                  {msg.role === "assistant" ? (
                    <AvatarFallback className="bg-primary text-primary-foreground"><Bot className="w-4 h-4" /></AvatarFallback>
                  ) : (
                    <AvatarFallback className="bg-muted text-muted-foreground"><User className="w-4 h-4" /></AvatarFallback>
                  )}
                </Avatar>
                
                <div className={`rounded-lg px-4 py-3 max-w-[80%] ${
                  msg.role === "user" 
                    ? "bg-primary text-primary-foreground" 
                    : "bg-muted"
                }`}>
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="flex gap-3">
                <Avatar className="h-8 w-8 shrink-0">
                  <AvatarFallback className="bg-primary text-primary-foreground"><Bot className="w-4 h-4" /></AvatarFallback>
                </Avatar>
                <div className="rounded-lg px-4 py-3 bg-muted flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
                  <span className="text-sm text-muted-foreground">JanSevak is typing...</span>
                </div>
              </div>
            )}
            <div ref={scrollRef} />
          </div>
        </ScrollArea>

        {/* Input Area */}
        <div className="p-4 border-t bg-card">
          <form onSubmit={handleSend} className="flex gap-2">
            <Input 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about PM Kisan, Ayushman Bharat, or local certificates..." 
              className="flex-1"
              disabled={isLoading}
            />
            <Button type="submit" disabled={isLoading || !input.trim()}>
              <Send className="w-4 h-4 mr-2" />
              Send
            </Button>
          </form>
          <p className="text-center text-[10px] text-muted-foreground mt-2">
            JanSevak AI can make mistakes. Always verify critical information at official portals.
          </p>
        </div>
      </div>
    </AppLayout>
  );
}
