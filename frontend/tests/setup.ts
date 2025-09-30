import { vi } from 'vitest';

// Mock Next.js modules
vi.mock('next/server', () => ({
  NextRequest: vi.fn().mockImplementation((url: string, init?: RequestInit) => ({
    url,
    nextUrl: {
      searchParams: new URLSearchParams(new URL(url).search),
    },
    json: vi.fn().mockResolvedValue(init?.body ? JSON.parse(init.body as string) : {}),
  })),
  NextResponse: {
    json: vi.fn().mockImplementation((data: any, init?: ResponseInit) => ({
      json: vi.fn().mockResolvedValue(data),
      status: init?.status || 200,
    })),
  },
}));

// Mock environment variables
process.env.DATABASE_URL = 'file:./test.db';
process.env.PYTHON_SERVICE_URL = 'http://localhost:8001';
process.env.NEXT_PUBLIC_API_URL = 'http://localhost:3000';

// Mock fetch globally
global.fetch = vi.fn();

// Suppress console.log in tests unless explicitly needed
vi.spyOn(console, 'log').mockImplementation(() => {});
vi.spyOn(console, 'error').mockImplementation(() => {});