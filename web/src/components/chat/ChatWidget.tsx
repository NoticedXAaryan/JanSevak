"use client";
import React, { useState } from "react";
import Image from "next/image";
import { MessageSquare, X, Maximize2 } from "lucide-react";
import ChatInput from "./ChatInput";
import MessageBubble from "./MessageBubble";
import Link from "next/link";

type Message = {
  id: string;
  role: "assistant" | "user";
  content: string;
  timestamp: string;
};

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hi! Need help finding a service or tracking a grievance?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 p-4 bg-primary text-primary-foreground rounded-full shadow-xl hover:bg-primary/90 transition-transform hover:scale-105 active:scale-95 z-50 flex items-center justify-center group"
      >
        <MessageSquare className="w-6 h-6" />
        <span className="absolute right-full mr-4 bg-card text-foreground px-3 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none shadow-lg border border-border">
          Ask JanSevak AI
        </span>
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 w-[350px] sm:w-[400px] h-[600px] max-h-[calc(100vh-3rem)] bg-background border border-border rounded-2xl shadow-2xl flex flex-col z-50 overflow-hidden animate-in slide-in-from-bottom-8">
      {/* Header */}
      <div className="h-14 bg-card border-b border-border flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <div className="relative w-8 h-8 rounded-xl overflow-hidden flex items-center justify-center bg-black">
            <Image src="/logo.png" alt="JanSevak Logo" width={32} height={32} className="object-contain p-1" />
          </div>
          <span className="font-heading font-semibold text-foreground">JanSevak AI</span>
        </div>
        <div className="flex items-center gap-1">
          <Link href="/chat" className="p-2 text-muted-foreground hover:text-foreground rounded-md transition-colors">
            <Maximize2 className="w-4 h-4" />
          </Link>
          <button 
            onClick={() => setIsOpen(false)}
            className="p-2 text-muted-foreground hover:text-foreground rounded-md transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
      </div>

      {/* Input */}
      <div className="p-3 bg-card border-t border-border">
        <ChatInput 
          onSend={async (content) => {
            const userMsgId = Date.now().toString();
            const assistantId = (Date.now() + 1).toString();
            
            setMessages(prev => [
              ...prev, 
              {
                id: userMsgId,
                role: "user",
                content,
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
              },
              {
                id: assistantId,
                role: "assistant",
                content: "",
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
              }
            ]);

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
          }} 
        />
      </div>
    </div>
  );
}
