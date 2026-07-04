"use client";
import React, { useState } from "react";
import ChatInput from "@/components/chat/ChatInput";
import MessageBubble from "@/components/chat/MessageBubble";
import { Sparkles, History, Settings, MoreVertical } from "lucide-react";

export default function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: "1",
      role: "assistant" as const,
      content: "Namaste! I am JanSevak, your AI assistant for all government services. How can I help you today?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);

  const handleSend = async (content: string) => {
    // Add user message
    const userMsg = {
      id: Date.now().toString(),
      role: "user" as const,
      content,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [...prev, userMsg]);

    const assistantId = (Date.now() + 1).toString();
    const assistantMsg = {
      id: assistantId,
      role: "assistant" as const,
      content: "",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    
    setMessages(prev => [...prev, assistantMsg]);

    const { ChatClient } = await import("@/lib/chat-api");
    const client = new ChatClient();
    
    client.sendMessageStream(content, {
      onMessage: (chunk) => {
        setMessages(prev => prev.map(msg => 
          msg.id === assistantId 
            ? { ...msg, content: msg.content + chunk } 
            : msg
        ));
      },
      onError: (err) => {
        setMessages(prev => prev.map(msg => 
          msg.id === assistantId 
            ? { ...msg, content: msg.content + "\n\n**Error:** Could not reach JanSevak AI." } 
            : msg
        ));
      }
    });
  };

  return (
    <div className="flex-1 w-full flex flex-col md:flex-row h-[calc(100vh-4rem)]">
      {/* Sidebar for History */}
      <div className="hidden md:flex w-64 border-r border-border bg-card/50 flex-col">
        <div className="p-4 border-b border-border flex items-center justify-between">
          <h2 className="font-heading font-semibold flex items-center gap-2">
            <History className="w-4 h-4" /> History
          </h2>
        </div>
        <div className="flex-1 overflow-y-auto p-2">
          <button className="w-full text-left p-3 rounded-lg bg-muted text-sm font-medium mb-1 truncate">
            How to apply for income...
          </button>
          <button className="w-full text-left p-3 rounded-lg hover:bg-muted text-sm font-medium text-muted-foreground transition-colors mb-1 truncate">
            Track grievance GRV-894
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative bg-background/50">
        <div className="h-14 border-b border-border flex items-center justify-between px-6 bg-card/50 backdrop-blur-md">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-primary" />
            <h1 className="font-heading font-semibold">JanSevak AI</h1>
            <span className="px-2 py-0.5 rounded-full bg-primary/10 text-primary text-xs font-medium ml-2">Beta</span>
          </div>
          <div className="flex items-center gap-2">
            <button className="p-2 text-muted-foreground hover:text-foreground rounded-md"><Settings className="w-5 h-5" /></button>
            <button className="p-2 text-muted-foreground hover:text-foreground rounded-md md:hidden"><MoreVertical className="w-5 h-5" /></button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-2">
          {messages.map(msg => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
        </div>

        <div className="p-4 bg-background border-t border-border">
          <div className="max-w-3xl mx-auto">
            <ChatInput onSend={handleSend} />
            <p className="text-center text-xs text-muted-foreground mt-3">
              JanSevak AI can make mistakes. Please verify important information on official portals.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
