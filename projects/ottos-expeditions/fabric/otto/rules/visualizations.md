---
otto:
  rule:
    alwaysApply: false
    description: Guidelines for creating effective data visualizations in artifacts. Fetch before creating charts, dashboards, or any visual representation of data.
    globs: []
    jinja: false
    keywords:
      - artifact
      - chart
      - dashboard
      - data viz
      - graph
      - plot
      - visualization
---

# Visualization Rules

Create high-quality data visualizations in React artifacts using Recharts, Plotly, or D3.

Your default style (unless otherwise instructed) should be that of a sophisticated,
highly interactive BI dashboard.

Your default key features:
- dark mode but supports both light mode via a toggle
- indicators when data is loading
- cross-element interaction & filtering
- advanced charts that go beyond the standard elements
- use professional looking icons over emoji

## Data Inputs

Use fine grain queries to explore the data and build a nuanced understanding. When connecting
data bindings, however, you can load up to 100,000 records per data binding. Explore your
data sets and if you can load all of the data and filter client-side, you should. If you
cannot, write queries to reduce the data volumes you load into your artifact.

DO NOT make up data for valid data sets.

## When to Use This Rule

When creating charts, dashboards, graphs, or any data visualization in artifacts.

## When NOT to Use

- For mermaid diagrams (use mermaid artifact type directly)
- For static images or screenshots
- For non-data visualizations (use HTML artifact)

## Chart Library Selection

| Use Case | Library |
|----------|---------|
| Standard charts (bar, line, pie, area) | **Recharts** (default) |
| Interactive/exploratory (zoom, pan, export) | **Plotly** |
| Custom/novel visualizations | **D3** |
| 3D visualizations | **Three.js** |

## Chart Type Selection

| Data Pattern | Recommended Chart |
|--------------|-------------------|
| Trends over time | Line chart or Area chart |
| Comparing categories | Bar chart (vertical or horizontal) |
| Part-to-whole relationships | Pie chart (≤6 slices) or Stacked bar |
| Distribution | Histogram or Box plot |
| Correlation between variables | Scatter plot |
| Multiple metrics over time | Composed chart or Multi-line |
| Hierarchical data | Treemap or Sunburst |
| Geographic data | Choropleth map (use Plotly) |

## Default Color Palette

These colors align with Ascend's design system. Use them as defaults when the user hasn't specified colors.

### Categorical Data (use in order)

```javascript
const COLORS = {
  primary: '#0ea5e9',   // Sky blue - main data series
  secondary: '#14b8a6', // Teal - secondary series
  tertiary: '#8b5cf6',  // Purple - third series
  quaternary: '#f59e0b', // Amber - fourth series
  quinary: '#ec4899',   // Pink - fifth series
};
```

### Status/Semantic Colors

```javascript
const STATUS_COLORS = {
  success: '#22c55e',  // Green
  error: '#ef4444',    // Red
  warning: '#eab308',  // Yellow
  info: '#0ea5e9',     // Blue
  neutral: '#6b7280',  // Gray
};
```

### Extended Palette (for many categories)

```javascript
const EXTENDED_PALETTE = [
  '#0ea5e9', '#14b8a6', '#8b5cf6', '#f59e0b', '#ec4899',
  '#06b6d4', '#10b981', '#6366f1', '#f97316', '#d946ef',
  '#0284c7', '#059669', '#4f46e5', '#ea580c', '#c026d3',
];
```

## Icons (lucide-react)

The sandbox pins `lucide-react@0.263.1`. Many newer icon names do NOT exist in this version and will cause a render failure. **Only import icons from the verified list below.** Do not guess icon names — if an icon is not on this list, pick the closest alternative that is.

### Verified icons (lucide-react@0.263.1)

**Navigation & arrows:** ArrowDown, ArrowLeft, ArrowRight, ArrowUp, ArrowUpDown, ChevronDown, ChevronLeft, ChevronRight, ChevronUp, ExternalLink, MoreHorizontal, MoreVertical, Menu, Move, Undo

**Charts & data:** Activity, BarChart, BarChart2, BarChart3, BarChart4, BarChartBig, BarChartHorizontal, LineChart, PieChart, TrendingDown, TrendingUp

**Layout & UI:** Circle, Grid, Hash, Kanban, Layers, LayoutDashboard, LayoutGrid, List, Minus, PanelLeft, PanelRight, Plus, SlidersHorizontal, Sliders, Square, Table, X, XCircle

**Status & feedback:** AlertCircle, AlertTriangle, Check, CheckCircle, CheckCircle2, HelpCircle, Info, Loader, Loader2, ThumbsDown, ThumbsUp, Zap

**Objects:** Bell, BookOpen, Box, Building, Building2, Calendar, Clock, Cloud, Cog, CreditCard, Database, DollarSign, File, FileText, Flag, FolderOpen, Globe, Heart, Home, Image, Key, Link, Lock, Mail, Map, MapPin, MessageCircle, MessageSquare, Monitor, Mountain, Package, Palette, Pencil, Pin, Save, Search, Send, Settings, Settings2, Share, Share2, Shield, ShoppingCart, Signal, Smartphone, Sparkles, Star, Sun, Moon, Tag, Target, Timer, Trash, Trash2, Trophy, Truck, Umbrella, User, UserPlus, Users, Wallet, Wand

**Actions:** Copy, Download, Eye, EyeOff, Filter, LogOut, Pencil, Play, Power, RefreshCcw, RefreshCw, RotateCcw, RotateCw, Shuffle, Upload, ZoomIn, ZoomOut

## Styling Defaults

- **Always use `ResponsiveContainer`** for Recharts (never hardcode width)
- **Cards**: `bg-white rounded-xl shadow-sm p-6`
- **Grid lines**: `stroke="#e5e7eb" strokeDasharray="3 3"`
- **Axis labels**: `stroke="#6b7280" fontSize={12}`

