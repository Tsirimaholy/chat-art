export interface ChatMessage {
  message: string;
}

export interface ChatResponse {
  answer: string;
  sources: string[];
}

export interface ChatError {
  error: string;
  details?: string;
}

export interface ChatWidgetState {
  messages: Array<{
    id: string;
    type: 'user' | 'bot';
    content: string;
    sources?: string[];
    timestamp: Date;
  }>;
  isLoading: boolean;
  error: string | null;
}