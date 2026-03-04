/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

/** NodeCard: displays node details in the sidebar/detail pane. */

import React from 'react';
import type { GraphNode } from '../types';
import { CATEGORY_COLORS } from '../types';
import { Button } from './Button';
import { Icon } from './Icon';

interface NodeCardProps {
  node: GraphNode;
  onExplain?: (node: GraphNode) => void;
  onClose?: () => void;
  explanation?: string | null;
  explanationLoading?: boolean;
}

export const NodeCard: React.FC<NodeCardProps> = ({
  node,
  onExplain,
  onClose,
  explanation,
  explanationLoading = false,
}) => {
  const categoryColor = CATEGORY_COLORS[node.category] || CATEGORY_COLORS.default;

  return (
    <div
      className="card animate-slide-up"
      role="region"
      aria-label={`Details for ${node.label}`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <span
            className="w-3 h-3 rounded-full flex-shrink-0"
            style={{ backgroundColor: categoryColor }}
            aria-hidden="true"
          />
          <h3 className="text-lg font-semibold text-text-high">
            {node.label}
          </h3>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-text-disabled hover:text-text-high transition-colors"
            aria-label="Close details"
          >
            <Icon name="close" size={16} />
          </button>
        )}
      </div>

      {/* Category badge */}
      <div className="mb-3">
        <span className="badge-primary">{node.category}</span>
      </div>

      {/* Description */}
      {node.description && (
        <p className="text-sm text-text-medium mb-3 leading-relaxed">
          {node.description}
        </p>
      )}

      {/* CID */}
      {node.cid && (
        <div className="mb-3 p-2 bg-surface rounded-lg">
          <p className="text-xs text-text-disabled font-mono truncate">
            CID: {node.cid}
          </p>
        </div>
      )}

      {/* Explain button */}
      {onExplain && (
        <div className="mt-3">
          <Button
            variant="secondary"
            size="sm"
            icon={<Icon name="explain" size={16} />}
            onClick={() => onExplain(node)}
            loading={explanationLoading}
          >
            Explain
          </Button>
        </div>
      )}

      {/* Explanation */}
      {explanation && (
        <div className="mt-3 p-3 bg-surface rounded-lg border border-border">
          <div className="flex items-center gap-1.5 mb-2">
            <Icon name="ai" size={14} className="text-accent" />
            <span className="text-xs font-medium text-accent">
              Suggested explanation
            </span>
            <span className="badge-accent text-[10px]">LLM ran locally</span>
          </div>
          <p className="text-sm text-text-medium leading-relaxed">
            {explanation}
          </p>
          <p className="text-[10px] text-text-disabled mt-2">
            This explanation was generated on your device. No data was sent externally.
          </p>
        </div>
      )}
    </div>
  );
};
