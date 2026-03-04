/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/

/** Tooltip component with delay and accessible labeling. */

import React, { useCallback, useRef, useState } from 'react';

type Placement = 'top' | 'bottom' | 'left' | 'right';

interface TooltipProps {
  content: string;
  placement?: Placement;
  delay?: number;
  children: React.ReactElement;
}

const placementClasses: Record<Placement, string> = {
  top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
  bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
  left: 'right-full top-1/2 -translate-y-1/2 mr-2',
  right: 'left-full top-1/2 -translate-y-1/2 ml-2',
};

export const Tooltip: React.FC<TooltipProps> = ({
  content,
  placement = 'top',
  delay = 300,
  children,
}) => {
  const [visible, setVisible] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout>>();

  const show = useCallback(() => {
    timeoutRef.current = setTimeout(() => setVisible(true), delay);
  }, [delay]);

  const hide = useCallback(() => {
    clearTimeout(timeoutRef.current);
    setVisible(false);
  }, []);

  return (
    <div className="relative inline-flex" onMouseEnter={show} onMouseLeave={hide} onFocus={show} onBlur={hide}>
      {children}
      {visible && (
        <div
          role="tooltip"
          className={`absolute z-50 px-2.5 py-1.5 text-xs font-medium text-text-high bg-elevated border border-border rounded-lg shadow-elevated whitespace-nowrap animate-fade-in ${placementClasses[placement]}`}
        >
          {content}
          <span className="sr-only">{content}</span>
        </div>
      )}
    </div>
  );
};
