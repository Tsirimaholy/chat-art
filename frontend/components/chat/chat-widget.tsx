"use client";

import { useState } from "react";
import type { ChatWidgetState } from "@/types/chat";
import { sendChatMessage, validateChatMessage, formatChatSources, generateMessageId } from "@/lib/chat";

export function ChatWidget() {
  const [state, setState] = useState<ChatWidgetState>({
    messages: [],
    isLoading: false,
    error: null,
  });
  const [inputMessage, setInputMessage] = useState("");

  const sendMessage = async (message: string) => {
    if (!message.trim()) return;

    const userMessage = {
      id: generateMessageId("user"),
      type: "user" as const,
      content: message,
      timestamp: new Date(),
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null,
    }));

    setInputMessage("");

    try {
      const data = await sendChatMessage(message);

      const botMessage = {
        id: generateMessageId("bot"),
        type: "bot" as const,
        content: data.answer,
        sources: data.sources,
        timestamp: new Date(),
      };

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, botMessage],
        isLoading: false,
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : "An error occurred",
      }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateChatMessage(inputMessage)) {
      sendMessage(inputMessage);
    }
  };

  return (
    <div className="bg-white border rounded-lg shadow-sm p-4 max-w-md">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">Finance FAQ Chat</h3>
      
      {/* Messages Container */}
      <div className="h-64 overflow-y-auto mb-4 space-y-2 border rounded p-2 bg-gray-50">
        {state.messages.length === 0 && (
          <div className="text-gray-500 text-sm text-center py-8">
            Ask me anything about finance! Try questions about EBITDA, margins, cash flow, etc.
          </div>
        )}
        
        {state.messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.type === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-xs px-3 py-2 rounded-lg text-sm ${
                msg.type === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-white border text-gray-800"
              }`}
            >
              <div>{msg.content}</div>
              {msg.sources && msg.sources.length > 0 && (
                <div className="mt-2 text-xs opacity-75">
                  <span className="font-medium">Sources:</span>{" "}
                  {formatChatSources(msg.sources)}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {state.isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border rounded-lg px-3 py-2 text-sm text-gray-600">
              <div className="flex items-center space-x-1">
                <div className="animate-bounce w-2 h-2 bg-gray-400 rounded-full"></div>
                <div className="animate-bounce w-2 h-2 bg-gray-400 rounded-full" style={{ animationDelay: "0.1s" }}></div>
                <div className="animate-bounce w-2 h-2 bg-gray-400 rounded-full" style={{ animationDelay: "0.2s" }}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Error Display */}
      {state.error && (
        <div className="mb-4 p-2 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
          Error: {state.error}
        </div>
      )}

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Ask a finance question..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={state.isLoading}
        />
        <button
          type="submit"
          disabled={state.isLoading || !validateChatMessage(inputMessage)}
          className="px-4 py-2 bg-blue-500 text-white rounded-md text-sm hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </form>
    </div>
  );
}