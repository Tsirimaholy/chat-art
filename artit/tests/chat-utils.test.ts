import { describe, it, expect } from 'vitest';
import { 
  validateChatMessage, 
  formatChatSources, 
  generateMessageId, 
  truncateMessage 
} from '@/lib/chat';

describe('Chat Utilities', () => {
  describe('validateChatMessage', () => {
    it('should return true for valid messages', () => {
      expect(validateChatMessage('Hello')).toBe(true);
      expect(validateChatMessage('What is EBITDA?')).toBe(true);
      expect(validateChatMessage('A'.repeat(100))).toBe(true);
      expect(validateChatMessage('A'.repeat(1000))).toBe(true);
    });

    it('should return false for empty or whitespace-only messages', () => {
      expect(validateChatMessage('')).toBe(false);
      expect(validateChatMessage('   ')).toBe(false);
      expect(validateChatMessage('\n\t  ')).toBe(false);
    });

    it('should return false for messages that are too long', () => {
      expect(validateChatMessage('A'.repeat(1001))).toBe(false);
      expect(validateChatMessage('A'.repeat(5000))).toBe(false);
    });
  });

  describe('formatChatSources', () => {
    it('should format FAQ sources correctly', () => {
      expect(formatChatSources(['faq#ebitda'])).toBe('FAQ: EBITDA');
      expect(formatChatSources(['faq#marge-brute'])).toBe('FAQ: MARGE BRUTE');
      expect(formatChatSources(['faq#cash-flow'])).toBe('FAQ: CASH FLOW');
    });

    it('should format system sources correctly', () => {
      expect(formatChatSources(['system#unavailable'])).toBe('System');
      expect(formatChatSources(['system#error'])).toBe('System');
    });

    it('should handle multiple sources', () => {
      expect(formatChatSources(['faq#ebitda', 'faq#marge-brute'])).toBe('FAQ: EBITDA, FAQ: MARGE BRUTE');
      expect(formatChatSources(['faq#ebitda', 'system#unavailable'])).toBe('FAQ: EBITDA, System');
    });

    it('should handle unknown source formats', () => {
      expect(formatChatSources(['unknown-source'])).toBe('unknown-source');
      expect(formatChatSources(['doc#article-1'])).toBe('doc#article-1');
    });

    it('should handle empty or invalid sources', () => {
      expect(formatChatSources([])).toBe('');
      expect(formatChatSources(null as any)).toBe('');
      expect(formatChatSources(undefined as any)).toBe('');
    });
  });

  describe('generateMessageId', () => {
    it('should generate unique IDs for user messages', () => {
      const id1 = generateMessageId('user');
      const id2 = generateMessageId('user');
      
      expect(id1).toMatch(/^user-\d+-.+$/);
      expect(id2).toMatch(/^user-\d+-.+$/);
      expect(id1).not.toBe(id2);
    });

    it('should generate unique IDs for bot messages', () => {
      const id1 = generateMessageId('bot');
      const id2 = generateMessageId('bot');
      
      expect(id1).toMatch(/^bot-\d+-.+$/);
      expect(id2).toMatch(/^bot-\d+-.+$/);
      expect(id1).not.toBe(id2);
    });

    it('should differentiate between user and bot IDs', () => {
      const userId = generateMessageId('user');
      const botId = generateMessageId('bot');
      
      expect(userId.startsWith('user-')).toBe(true);
      expect(botId.startsWith('bot-')).toBe(true);
      expect(userId).not.toBe(botId);
    });
  });

  describe('truncateMessage', () => {
    it('should not truncate messages shorter than max length', () => {
      const shortMessage = 'This is a short message';
      expect(truncateMessage(shortMessage)).toBe(shortMessage);
      expect(truncateMessage(shortMessage, 100)).toBe(shortMessage);
    });

    it('should truncate messages longer than max length', () => {
      const longMessage = 'A'.repeat(600);
      const truncated = truncateMessage(longMessage);
      
      expect(truncated).toBe('A'.repeat(500) + '...');
      expect(truncated.length).toBe(503); // 500 + '...'
    });

    it('should respect custom max length', () => {
      const message = 'A'.repeat(200);
      const truncated = truncateMessage(message, 50);
      
      expect(truncated).toBe('A'.repeat(50) + '...');
      expect(truncated.length).toBe(53);
    });

    it('should handle edge cases', () => {
      expect(truncateMessage('')).toBe('');
      expect(truncateMessage('A', 1)).toBe('A');
      expect(truncateMessage('AB', 1)).toBe('A...');
    });
  });
});