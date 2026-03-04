# Design System

## TL;DR

Project Mycelium's design system is dark-theme-first with high contrast,
accessible typography, and a programmable light toggle. All tokens are
defined as CSS variables and extended into Tailwind.

---

## Color Tokens

### Dark Theme (Default)

| Token | Hex | Usage | Contrast Ratio (on surface) |
|-------|-----|-------|-----------------------------|
| `--color-primary` | `#6D9BF1` | Primary actions, links | 5.2:1 |
| `--color-secondary` | `#A78BFA` | Secondary actions | 4.8:1 |
| `--color-accent` | `#34D399` | Highlights, success | 5.5:1 |
| `--color-surface` | `#0F1117` | Base background | — |
| `--color-elevated` | `#1A1D2E` | Cards, panels | — |
| `--color-text-high` | `#F1F5F9` | Primary text | 15.8:1 |
| `--color-text-medium` | `#94A3B8` | Secondary text | 5.3:1 |
| `--color-text-disabled` | `#475569` | Disabled text | 2.8:1 |
| `--color-success` | `#22C55E` | Success states | 4.5:1 |
| `--color-warn` | `#F59E0B` | Warning states | 4.6:1 |
| `--color-danger` | `#EF4444` | Error, destructive | 4.5:1 |
| `--color-border` | `#2D3348` | Borders, dividers | — |

### Light Theme

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-primary` | `#3B6FD4` | Primary actions |
| `--color-secondary` | `#7C3AED` | Secondary actions |
| `--color-accent` | `#059669` | Highlights |
| `--color-surface` | `#FFFFFF` | Base background |
| `--color-elevated` | `#F8FAFC` | Cards, panels |
| `--color-text-high` | `#0F172A` | Primary text |
| `--color-text-medium` | `#475569` | Secondary text |
| `--color-text-disabled` | `#94A3B8` | Disabled text |

---

## Typography

### Font Stack

```css
--font-sans: 'Inter Variable', 'Inter', system-ui, -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, monospace;
```

### Scale

| Level | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| `text-xs` | 12px | 400 | 1.5 | Captions, badges |
| `text-sm` | 14px | 400 | 1.5 | Helper text |
| `text-base` | 16px | 400 | 1.5 | Body text |
| `text-lg` | 18px | 500 | 1.4 | Subheadings |
| `text-xl` | 20px | 600 | 1.3 | Section titles |
| `text-2xl` | 24px | 700 | 1.2 | Page titles |
| `text-3xl` | 30px | 700 | 1.1 | Hero titles |
| `text-presenter` | 40px | 800 | 1.0 | Presenter mode only |

---

## Spacing Scale

Based on a 4px grid:

| Token | Value | Usage |
|-------|-------|-------|
| `space-1` | 4px | Tight gaps |
| `space-2` | 8px | Element gaps |
| `space-3` | 12px | Component padding |
| `space-4` | 16px | Section padding |
| `space-6` | 24px | Card padding |
| `space-8` | 32px | Section margins |
| `space-12` | 48px | Layout gaps |
| `space-16` | 64px | Page margins |

---

## Component Library

### Button

Variants: `primary`, `secondary`, `ghost`, `danger`
Sizes: `sm`, `md`, `lg`
States: `default`, `hover`, `active`, `focus`, `disabled`

```tsx
<Button variant="primary" size="md">Save Graph</Button>
<Button variant="ghost" size="sm" icon={<SearchIcon />}>Search</Button>
```

### Input

Variants: `default`, `search`, `error`
Features: label, helper text, error message, leading icon

```tsx
<Input
  label="Node Label"
  placeholder="Enter node name..."
  error={errors.label}
  leadingIcon={<TagIcon />}
/>
```

### Modal

Features: focus trap, escape to close, backdrop click, ARIA

```tsx
<Modal open={isOpen} onClose={handleClose} title="Node Details">
  <NodeDetailContent node={selectedNode} />
</Modal>
```

### Tooltip

Placement: `top`, `bottom`, `left`, `right`
Triggers: hover (300ms delay), focus

```tsx
<Tooltip content="Click to expand details" placement="top">
  <Button>Details</Button>
</Tooltip>
```

### Switch

Features: ARIA role="switch", keyboard toggle, label

```tsx
<Switch
  checked={darkMode}
  onChange={setDarkMode}
  label="Dark theme"
/>
```

### NodeCard

Features: category badge, description, actions, keyboard focus

```tsx
<NodeCard
  node={node}
  onExpand={handleExpand}
  onExplain={handleExplain}
/>
```

### GraphCanvas

Features: pan, zoom, node selection, edge highlighting, LOD

```tsx
<GraphCanvas
  nodes={nodes}
  edges={edges}
  onNodeClick={handleNodeClick}
  presenterMode={isPresenter}
/>
```

---

## Icon System

SVG sprite sheet at `src/frontend/public/icons.svg`.
Usage:

```tsx
<Icon name="search" size={20} className="text-text-medium" />
<Icon name="graph" size={24} className="text-primary" />
```

Available icons: `search`, `graph`, `node`, `edge`, `lock`, `unlock`,
`sync`, `offline`, `ai`, `explain`, `export`, `settings`, `sun`, `moon`,
`close`, `menu`, `arrow-right`, `arrow-left`, `check`, `warning`, `info`.

---

## Motion

### Durations

| Token | Value | Usage |
|-------|-------|-------|
| `duration-fast` | 100ms | Hover, press |
| `duration-normal` | 200ms | Transitions |
| `duration-slow` | 300ms | Modal, panel |
| `duration-graph` | 500ms | Graph animations |

### Easing

| Token | Value | Usage |
|-------|-------|-------|
| `ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Enter |
| `ease-in` | `cubic-bezier(0.7, 0, 0.84, 0)` | Exit |
| `ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Bounce |

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Accessibility

- All interactive elements have visible focus outlines (2px solid primary).
- Color is never the sole indicator — icons and text supplement.
- ARIA labels on all icon-only buttons.
- Screen reader announcements for graph interactions.
- Tab order follows visual layout.
- Focus trap in modals and drawers.
- Minimum touch target: 44x44px.

---

Copyright (c) 2026 Zorvia Community. Licensed under ZPL v2.0.
