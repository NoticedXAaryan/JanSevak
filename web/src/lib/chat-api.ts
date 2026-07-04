/**
 * Client for interacting with the JanSevak FastAPI Chat/Agent endpoints via SSE.
 */

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
}

export interface ChatOptions {
  onMessage?: (chunk: string) => void;
  onError?: (error: Error) => void;
  onFinish?: (fullMessage: string) => void;
  signal?: AbortSignal;
}

export class ChatClient {
  private endpoint: string;

  constructor(endpoint: string = "/api/v1/chat/stream") {
    // In dev, assuming proxy or full URL.
    this.endpoint = process.env.NEXT_PUBLIC_API_URL 
      ? `${process.env.NEXT_PUBLIC_API_URL}/chat/stream` 
      : "http://localhost:8000/api/v1/chat/stream";
  }

  /**
   * Send a message and stream the response via Server-Sent Events.
   */
  async sendMessageStream(message: string, options: ChatOptions = {}) {
    try {
      const response = await fetch(this.endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // Add auth if needed
        },
        body: JSON.stringify({ message }),
        signal: options.signal,
      });

      if (!response.ok || !response.body) {
        throw new Error(`Failed to connect to chat stream: ${response.statusText}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullMessage = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        // The backend should send SSE formatted data: "data: {...}\n\n"
        const lines = chunk.split("\n");
        
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const dataStr = line.slice(6);
            if (dataStr === "[DONE]") {
              break;
            }
            try {
              const data = JSON.parse(dataStr);
              if (data.content) {
                fullMessage += data.content;
                options.onMessage?.(data.content);
              }
            } catch (e) {
              console.warn("Failed to parse SSE data chunk:", dataStr);
            }
          }
        }
      }

      options.onFinish?.(fullMessage);
    } catch (error) {
      if (error instanceof Error && error.name === "AbortError") {
        console.log("Chat stream aborted");
      } else {
        options.onError?.(error instanceof Error ? error : new Error(String(error)));
      }
    }
  }
}
