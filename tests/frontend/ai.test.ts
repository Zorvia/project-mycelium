/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

import { describe, it, expect } from 'vitest';
import {
  StubSummarizer,
  createLLMAdapter,
} from '../../src/ai/LocalLLMAdapter';

describe('StubSummarizer', () => {
  const stub = new StubSummarizer();

  it('should have correct metadata', () => {
    expect(stub.name).toBe('StubSummarizer');
    expect(stub.isLocal).toBe(true);
    expect(stub.isAvailable()).toBe(true);
  });

  it('should summarize deterministically', async () => {
    const result = await stub.summarize('Physics is interesting');
    expect(result).toContain('Physics');
    expect(result.length).toBeGreaterThan(0);
  });

  it('should produce same summary for same input', async () => {
    const a = await stub.summarize('Test content');
    const b = await stub.summarize('Test content');
    expect(a).toBe(b);
  });

  it('should explain a topic', async () => {
    const result = await stub.explain('Quantum Mechanics', 'The study of quantum phenomena');
    expect(result).toContain('Quantum Mechanics');
  });

  it('should handle empty input', async () => {
    const result = await stub.summarize('');
    expect(typeof result).toBe('string');
  });
});

describe('createLLMAdapter', () => {
  it('should return an adapter', () => {
    const adapter = createLLMAdapter();
    expect(adapter).toBeDefined();
    expect(adapter.name).toBeTruthy();
    expect(typeof adapter.isLocal).toBe('boolean');
    expect(typeof adapter.isAvailable).toBe('function');
    expect(typeof adapter.summarize).toBe('function');
    expect(typeof adapter.explain).toBe('function');
  });

  it('should return StubSummarizer when WebGPU is unavailable', () => {
    // In test environment, navigator.gpu is not available
    const adapter = createLLMAdapter();
    expect(adapter.name).toBe('StubSummarizer');
  });
});
