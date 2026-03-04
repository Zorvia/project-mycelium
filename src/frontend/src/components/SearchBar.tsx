/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

/** Search with autocomplete and keyboard navigation. */

import React, { useCallback, useEffect, useRef, useState } from 'react';
import type { GraphNode } from '../types';
import { Icon } from './Icon';

interface SearchBarProps {
  nodes: GraphNode[];
  onSelect: (node: GraphNode) => void;
  placeholder?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  nodes,
  onSelect,
  placeholder = 'Search nodes...',
}) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<GraphNode[]>([]);
  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLUListElement>(null);

  // Filter nodes
  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      setOpen(false);
      return;
    }
    const q = query.toLowerCase();
    const filtered = nodes
      .filter(
        (n) =>
          n.label.toLowerCase().includes(q) ||
          n.category.toLowerCase().includes(q) ||
          n.description?.toLowerCase().includes(q),
      )
      .slice(0, 8);
    setResults(filtered);
    setOpen(filtered.length > 0);
    setActiveIndex(-1);
  }, [query, nodes]);

  const handleSelect = useCallback(
    (node: GraphNode) => {
      onSelect(node);
      setQuery(node.label);
      setOpen(false);
      inputRef.current?.blur();
    },
    [onSelect],
  );

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (!open) return;
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          setActiveIndex((i) => Math.min(i + 1, results.length - 1));
          break;
        case 'ArrowUp':
          e.preventDefault();
          setActiveIndex((i) => Math.max(i - 1, 0));
          break;
        case 'Enter':
          e.preventDefault();
          if (activeIndex >= 0 && results[activeIndex]) {
            handleSelect(results[activeIndex]);
          }
          break;
        case 'Escape':
          setOpen(false);
          break;
      }
    },
    [open, activeIndex, results, handleSelect],
  );

  return (
    <div className="relative" role="combobox" aria-expanded={open} aria-haspopup="listbox">
      <div className="relative">
        <Icon
          name="search"
          size={16}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-text-disabled"
        />
        <input
          ref={inputRef}
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => results.length > 0 && setOpen(true)}
          onBlur={() => setTimeout(() => setOpen(false), 200)}
          placeholder={placeholder}
          className="input-base pl-9 pr-3"
          role="searchbox"
          aria-autocomplete="list"
          aria-controls="search-results"
          aria-activedescendant={
            activeIndex >= 0 ? `search-result-${activeIndex}` : undefined
          }
          aria-label="Search knowledge graph nodes"
        />
      </div>

      {/* Results dropdown */}
      {open && (
        <ul
          ref={listRef}
          id="search-results"
          role="listbox"
          className="absolute z-40 w-full mt-1 bg-elevated border border-border rounded-xl shadow-elevated overflow-hidden animate-slide-up"
        >
          {results.map((node, i) => (
            <li
              key={node.id}
              id={`search-result-${i}`}
              role="option"
              aria-selected={i === activeIndex}
              className={`px-3 py-2 cursor-pointer flex items-center gap-2 transition-colors
                ${i === activeIndex ? 'bg-primary/10 text-text-high' : 'text-text-medium hover:bg-surface'}`}
              onMouseDown={() => handleSelect(node)}
              onMouseEnter={() => setActiveIndex(i)}
            >
              <span
                className="w-2 h-2 rounded-full flex-shrink-0"
                style={{
                  backgroundColor:
                    node.category === 'default' ? '#94A3B8' : undefined,
                }}
                aria-hidden="true"
              />
              <span className="text-sm truncate">{node.label}</span>
              <span className="text-xs text-text-disabled ml-auto">
                {node.category}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
