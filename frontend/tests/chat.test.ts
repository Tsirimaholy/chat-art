import { describe, it, expect, vi, beforeEach } from 'vitest';
import { NextRequest } from 'next/server';
import { POST } from '@/app/api/chat/route';

// Mock fetch globally
global.fetch = vi.fn();

describe('/api/chat', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset environment variables
    process.env.PYTHON_SERVICE_URL = 'http://localhost:8001';
  });

  it('should return a successful response when Python service is available', async () => {
    // Mock successful Python service response
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        answer: 'EBITDA is an indicator of operational performance before interests, taxes, depreciation and amortization.',
        sources: ['faq#ebitda']
      })
    });

    const request = new NextRequest('http://localhost:3000/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message: 'What is EBITDA?' }),
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data).toEqual({
      answer: 'EBITDA is an indicator of operational performance before interests, taxes, depreciation and amortization.',
      sources: ['faq#ebitda']
    });
    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8001/chat',
      expect.objectContaining({
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: 'What is EBITDA?' }),
      })
    );
  });

  it('should return 400 for invalid request body', async () => {
    const request = new NextRequest('http://localhost:3000/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message: '' }), // Empty message
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(400);
    expect(data.error).toBe('Invalid request');
  });

  it('should return mock response when Python service is unavailable', async () => {
    // Mock fetch to throw a network error
    (global.fetch as any).mockRejectedValueOnce(new TypeError('fetch failed'));

    const request = new NextRequest('http://localhost:3000/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message: 'What is EBITDA?' }),
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data).toEqual({
      answer: "I'm sorry, the chat service is currently unavailable. Please try again later.",
      sources: ['system#unavailable']
    });
  });

  it('should handle Python service error responses', async () => {
    // Mock Python service returning an error
    (global.fetch as any).mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    const request = new NextRequest('http://localhost:3000/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message: 'What is EBITDA?' }),
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(500);
    expect(data.error).toBe('Internal server error');
  });

  it('should validate message is not empty', async () => {
    const request = new NextRequest('http://localhost:3000/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message: '' }), // Empty string
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(400);
    expect(data.error).toBe('Invalid request');
    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('should handle malformed JSON request', async () => {
    const request = new NextRequest('http://localhost:3000/api/chat', {
      method: 'POST',
      body: 'invalid json',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(500);
    expect(data.error).toBe('Internal server error');
  });
});