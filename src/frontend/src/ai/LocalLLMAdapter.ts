/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

/**
 * Local LLM Adapter — modular interface for on-device AI.
 *
 * Two implementations:
 * 1. StubSummarizer — deterministic template-based (always available)
 * 2. WebGPUModelAdapter — optional, requires user-supplied model files
 *
 * IMPORTANT: No data is ever sent to external servers.
 */

// ─── Interface ─────────────────────────────────

export interface LocalLLMAdapter {
  readonly name: string;
  readonly isLocal: boolean;
  isAvailable(): Promise<boolean>;
  summarize(label: string, category: string, description: string): Promise<string>;
  explain(label: string, context: string): Promise<string>;
}

// ─── StubSummarizer ────────────────────────────

/**
 * Deterministic template-based summarizer.
 * Always available, no GPU required.
 * Produces consistent, readable explanations.
 */
export class StubSummarizer implements LocalLLMAdapter {
  readonly name = 'StubSummarizer';
  readonly isLocal = true;

  async isAvailable(): Promise<boolean> {
    return true;
  }

  async summarize(
    label: string,
    category: string,
    description: string,
  ): Promise<string> {
    const categoryName = category.replace(/_/g, ' ');
    if (description && description.length > 20) {
      return `${label} is a concept in ${categoryName}. ${description.slice(0, 200)}${description.length > 200 ? '...' : ''}`;
    }
    return `${label} is a key concept in the field of ${categoryName}. It connects to several related topics in the knowledge graph, forming an important part of the broader understanding of ${categoryName}.`;
  }

  async explain(label: string, context: string): Promise<string> {
    const connections = context
      ? ` It is connected to ${context}.`
      : '';
    return `${label} represents an important concept in this knowledge graph.${connections} Understanding ${label} helps build a more complete picture of the topic. This explanation was generated locally using template-based summarization.`;
  }
}

// ─── WebGPUModelAdapter ────────────────────────

/**
 * Optional WebGPU-powered model adapter.
 * Requires user to supply model files.
 * Uses WebLLM or similar WASM/WebGPU runtime.
 */
export class WebGPUModelAdapter implements LocalLLMAdapter {
  readonly name = 'WebGPU LLM';
  readonly isLocal = true;
  private _modelLoaded = false;

  async isAvailable(): Promise<boolean> {
    // Check for WebGPU support
    if (typeof navigator === 'undefined') return false;
    if (!('gpu' in navigator)) return false;
    try {
      const adapter = await (navigator as unknown as { gpu: { requestAdapter: () => Promise<unknown> } }).gpu.requestAdapter();
      return adapter !== null;
    } catch {
      return false;
    }
  }

  async summarize(
    label: string,
    category: string,
    description: string,
  ): Promise<string> {
    if (!this._modelLoaded) {
      // Fall back to stub
      const stub = new StubSummarizer();
      return stub.summarize(label, category, description);
    }
    // In a full implementation, this would:
    // 1. Tokenize the input
    // 2. Run inference on the WebGPU model
    // 3. Decode the output tokens
    return `[WebGPU] Summary for ${label}: ${description || 'A concept in ' + category}`;
  }

  async explain(label: string, context: string): Promise<string> {
    if (!this._modelLoaded) {
      const stub = new StubSummarizer();
      return stub.explain(label, context);
    }
    return `[WebGPU] Explanation for ${label} in context of ${context}`;
  }

  /**
   * Load a model from user-supplied files.
   * This is documented but not required for the demo.
   */
  async loadModel(_modelPath: string): Promise<void> {
    const available = await this.isAvailable();
    if (!available) {
      throw new Error('WebGPU is not available in this browser');
    }
    // Model loading would happen here
    this._modelLoaded = true;
  }
}

// ─── Factory ───────────────────────────────────

/**
 * Create the best available LLM adapter.
 * Falls back to StubSummarizer if WebGPU isn't available.
 */
export async function createLLMAdapter(): Promise<LocalLLMAdapter> {
  const webgpu = new WebGPUModelAdapter();
  if (await webgpu.isAvailable()) {
    console.log('[AI] WebGPU available — using WebGPUModelAdapter (model loading required)');
    // Note: model must still be loaded separately
    // For demo, fall through to stub
  }
  console.log('[AI] Using StubSummarizer (deterministic, always available)');
  return new StubSummarizer();
}
