import type { ChatMessage, ChatResponse } from "@/types/chat";

/**
 * Sends a chat message to the API and returns the response
 */
export async function sendChatMessage(message: string): Promise<ChatResponse> {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message } satisfies ChatMessage),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Network error" }));
    throw new Error(error.error || `HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/**
 * Validates if a message is valid for sending
 */
export function validateChatMessage(message: string): boolean {
  return message.trim().length > 0 && message.length <= 1000;
}

/**
 * Formats chat sources for display
 */
export function formatChatSources(sources: string[]): string {
  if (!sources || sources.length === 0) return "";
  
  return sources
    .map(source => {
      // Convert "faq#ebitda" to "FAQ: EBITDA"
      if (source.startsWith("faq#")) {
        const topic = source.replace("faq#", "").toUpperCase().replace("-", " ");
        return `FAQ: ${topic}`;
      }
      // Convert "system#unavailable" to "System"
      if (source.startsWith("system#")) {
        return "System";
      }
      return source;
    })
    .join(", ");
}

/**
 * Generates a unique ID for chat messages
 */
export function generateMessageId(type: "user" | "bot"): string {
  return `${type}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Truncates long messages for display
 */
export function truncateMessage(message: string, maxLength: number = 500): string {
  if (message.length <= maxLength) return message;
  return message.substring(0, maxLength) + "...";
}