import React from "react";
import { Send, Mic, Paperclip } from "lucide-react";

export default function ChatInput({ 
  onSend, 
  disabled 
}: { 
  onSend: (msg: string) => void;
  disabled?: boolean;
}) {
  const [input, setInput] = React.useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input);
      setInput("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative w-full">
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center">
        <button type="button" className="p-2 text-muted-foreground hover:text-foreground rounded-full hover:bg-muted transition-colors">
          <Paperclip className="w-5 h-5" />
        </button>
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={disabled}
        placeholder="Type a message..."
        className="w-full pl-12 pr-24 py-4 bg-background border border-border rounded-full text-foreground placeholder-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all shadow-sm disabled:opacity-50"
      />
      <div className="absolute inset-y-1.5 right-1.5 flex items-center gap-1">
        <button type="button" className="p-2.5 text-muted-foreground hover:text-foreground rounded-full hover:bg-muted transition-colors">
          <Mic className="w-5 h-5" />
        </button>
        <button 
          type="submit" 
          disabled={!input.trim() || disabled}
          className="p-2.5 bg-primary text-primary-foreground rounded-full hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:hover:bg-primary"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
    </form>
  );
}
