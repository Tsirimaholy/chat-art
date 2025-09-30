"use client";

import React from "react";

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  errorInfo?: React.ErrorInfo;
}

interface ChatErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ComponentType<{ error: Error; retry: () => void }>;
}

export class ChatErrorBoundary extends React.Component<
  ChatErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ChatErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("Chat Error Boundary caught an error:", error, errorInfo);
    this.setState({
      error,
      errorInfo,
    });
  }

  retry = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
  };

  render() {
    if (this.state.hasError) {
      const FallbackComponent = this.props.fallback || DefaultErrorFallback;
      return (
        <FallbackComponent 
          error={this.state.error as Error} 
          retry={this.retry} 
        />
      );
    }

    return this.props.children;
  }
}

interface DefaultErrorFallbackProps {
  error: Error;
  retry: () => void;
}

function DefaultErrorFallback({ error, retry }: DefaultErrorFallbackProps) {
  return (
    <div className="bg-white border rounded-lg shadow-sm p-4 max-w-md">
      <div className="text-center">
        <div className="text-red-500 mb-2">
          <svg className="w-8 h-8 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-labelledby="error-icon-title">
            <title id="error-icon-title">Error icon</title>
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 18.5c-.77.833.192 2.5 1.732 2.5z" 
            />
          </svg>
        </div>
        <h3 className="text-lg font-semibold mb-2 text-gray-800">Chat Unavailable</h3>
        <p className="text-gray-600 text-sm mb-4">
          The chat widget encountered an error. This might be due to a network issue or server problem.
        </p>
        <div className="space-y-2">
          <button
            type="button"
            onClick={retry}
            className="w-full px-4 py-2 bg-blue-500 text-white rounded-md text-sm hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Try Again
          </button>
          <details className="text-left">
            <summary className="text-xs text-gray-500 cursor-pointer hover:text-gray-700">
              Error Details
            </summary>
            <pre className="text-xs text-red-600 mt-2 p-2 bg-red-50 rounded overflow-auto max-h-24">
              {error.message}
            </pre>
          </details>
        </div>
      </div>
    </div>
  );
}

/**
 * Hook to use error boundary for async operations
 */
export function useErrorBoundary() {
  const [error, setError] = React.useState<Error | null>(null);

  const resetError = React.useCallback(() => {
    setError(null);
  }, []);

  const captureError = React.useCallback((error: Error | string) => {
    const errorObj = typeof error === 'string' ? new Error(error) : error;
    setError(errorObj);
  }, []);

  React.useEffect(() => {
    if (error) {
      throw error;
    }
  }, [error]);

  return { captureError, resetError };
}