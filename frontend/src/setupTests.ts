import '@testing-library/jest-dom';
import { mockIntersectionObserver, mockResizeObserver, mockMatchMedia } from './utils/testUtils';

// Setup global mocks
beforeAll(() => {
  mockIntersectionObserver();
  mockResizeObserver();
  mockMatchMedia();
});

// Cleanup after each test
afterEach(() => {
  jest.clearAllMocks();
  jest.clearAllTimers();
});

// Mock console methods to reduce noise in tests
global.console = {
  ...console,
  error: jest.fn(),
  warn: jest.fn(),
  log: jest.fn(),
};