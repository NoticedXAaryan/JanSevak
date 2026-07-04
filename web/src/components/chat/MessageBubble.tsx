import React from "react";

interface MessageProps {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: string;
}

export default function MessageBubble({ message }: { message: MessageProps }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex w-full mb-6 ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`flex max-w-[80%] md:max-w-[70%] ${isUser ? "flex-row-reverse" : "flex-row"} items-end gap-2`}>
        
        {!isUser && (
          <div className="w-8 h-8 rounded-full bg-primary/20 border border-primary/30 flex flex-shrink-0 items-center justify-center">
            <span className="font-heading font-bold text-xs text-primary">JS</span>
          </div>
        )}

        <div className={`relative px-4 py-3 rounded-2xl ${
          isUser 
            ? "bg-primary text-primary-foreground rounded-br-sm" 
            : "bg-card border border-border text-foreground rounded-bl-sm"
        }`}>
          <div className="prose prose-sm dark:prose-invert max-w-none">
            {message.content.split('\n').map((line, i) => (
              <p key={i} className="mb-2 last:mb-0 leading-relaxed">{line}</p>
            ))}
          </div>
          <div className={`text-[10px] mt-2 opacity-60 ${isUser ? "text-right" : "text-left"}`}>
            {message.timestamp}
          </div>
        </div>
      </div>
    </div>
  );
}
