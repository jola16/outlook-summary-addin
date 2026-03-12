# Architecture – Outlook Summary Add-in

## Overview

The Outlook Summary Add-in is a lightweight, single-file Office add-in that integrates with Microsoft Outlook to display email summaries and actionable items in a taskpane sidebar.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Outlook Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Outlook Taskpane (Iframe Sandbox)           │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │  taskpane.html (Single-File Application)      │ │  │
│  │  │                                                │ │  │
│  │  │  ┌──────────────────────────────────────────┐ │ │  │
│  │  │  │  HTML Structure                         │ │ │  │
│  │  │  │  - Header (sender, subject, tabs)       │ │ │  │
│  │  │  │  - Content (scrollable panes)           │ │ │  │
│  │  │  │  - Status bar (feedback)                │ │ │  │
│  │  │  └──────────────────────────────────────────┘ │ │  │
│  │  │                                                │ │  │
│  │  │  ┌──────────────────────────────────────────┐ │ │  │
│  │  │  │  CSS Styling                            │ │ │  │
│  │  │  │  - Segoe UI design system               │ │ │  │
│  │  │  │  - Flexbox layout                       │ │ │  │
│  │  │  │  - Responsive design                    │ │ │  │
│  │  │  └──────────────────────────────────────────┘ │ │  │
│  │  │                                                │ │  │
│  │  │  ┌──────────────────────────────────────────┐ │ │  │
│  │  │  │  JavaScript Logic                       │ │ │  │
│  │  │  │  - Office.js API integration            │ │ │  │
│  │  │  │  - Custom properties management         │ │ │  │
│  │  │  │  - Tab switching                        │ │ │  │
│  │  │  │  - i18n (Swedish/English)               │ │ │  │
│  │  │  │  - Error handling                       │ │ │  │
│  │  │  └──────────────────────────────────────────┘ │ │  │
│  │  │                                                │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │  Office.js Library                           │ │  │
│  │  │  - Mailbox API                               │ │  │
│  │  │  - Custom Properties API                     │ │  │
│  │  │  - Async operations                          │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Email Item (Office.context.mailbox.item)          │  │
│  │  - Subject, From, To                               │  │
│  │  - Custom Properties (summary, actions)            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. HTML Structure

The taskpane is organized into three main sections:

```html
<body>
  <div id="header">
    <!-- Sender, recipient count, subject -->
    <!-- Tab navigation buttons -->
  </div>

  <div id="content">
    <!-- Loading indicator -->
    <!-- Actions pane -->
    <!-- Summary pane -->
  </div>

  <div id="status">
    <!-- Status messages (loading, saving, error, success) -->
  </div>
</body>
```

### 2. CSS Architecture

Styles are organized by functional area:

- **Global**: Box-sizing, body layout (flexbox column)
- **Header**: Metadata display, subject, tab buttons
- **Content**: Scrollable area, HTML content rendering
- **Status Bar**: Status messages with color coding
- **Loading**: Centered loading indicator

Color scheme:
- Background: `#fafaf8` (light beige)
- Text: `#1a1a1a` (dark gray)
- Borders: `#e8e5e0` (light gray)
- Status colors:
  - Error: `#c50f1f` (red)
  - Saving: `#ca5010` (orange)
  - Success: `#107c10` (green)

### 3. JavaScript Architecture

#### Initialization Flow

```
1. Office.onReady()
   ↓
2. Get current email item
   ↓
3. Display sender, recipient count, subject
   ↓
4. Load custom properties
   ↓
5. Check for existing summary/actions
   ↓
6. If missing: generate fallback + save
   ↓
7. Display content and enable tab switching
```

#### Key Functions

| Function | Purpose |
|----------|---------|
| `Office.onReady()` | Bootstrap: initialize when Office.js is ready |
| `onPropsLoaded()` | Handle custom properties load result |
| `showContent()` | Render summary and actions to DOM |
| `switchTab()` | Toggle between Actions and Summary views |
| `setStatus()` | Update status bar with message and type |

#### State Management

```javascript
let currentTab = "actions";  // Track active tab
```

Minimal state design: only tracks current tab. All other data flows through async callbacks.

#### Localization (i18n)

```javascript
const isSv = navigator.language.toLowerCase().startsWith("sv");

const t = {
  // All UI strings with Swedish and English variants
  tabActions: isSv ? "Åtgärder" : "Actions",
  // ...
};
```

Language detection is automatic; no user configuration needed.

## Data Flow

### Loading Custom Properties

```
User opens email
    ↓
Office.onReady() fires
    ↓
item.loadCustomPropertiesAsync(onPropsLoaded)
    ↓
onPropsLoaded() receives result
    ↓
Check if summary/actions exist
    ├─ YES: Display immediately
    └─ NO: Generate fallback + save
         ↓
         props.saveAsync(callback)
         ↓
         Display content
```

### Saving Custom Properties

```
props.set("summary", htmlContent)
props.set("actions", htmlContent)
    ↓
props.saveAsync(callback)
    ↓
Callback receives result
    ├─ SUCCESS: Show success message
    └─ ERROR: Show error message
```

## Custom Properties Schema

The add-in stores two properties in the email's custom properties:

| Property | Type | Description |
|----------|------|-------------|
| `summary` | HTML string | Summary content for Summary tab |
| `actions` | HTML string | Actions content for Actions tab |

**Namespace**: `cecp-357113F9-C204-44CA-A3FC-101588AF3F49`

This namespace is derived from the add-in's unique ID in `manifest.xml`.

## Error Handling

The add-in implements graceful error handling:

1. **Custom Properties Load Failure**
   - Display error message in status bar
   - Show empty content
   - User can retry by reopening email

2. **Custom Properties Save Failure**
   - Display error message in status bar
   - Content remains visible
   - User can retry or close/reopen

3. **Missing Data**
   - Fallback to sample content
   - Automatically save fallback
   - User sees working add-in even without real data

## Performance Considerations

- **Single-file architecture**: No network requests for code (only Office.js)
- **Minimal DOM manipulation**: Direct innerHTML updates
- **Async operations**: All Office.js calls are non-blocking
- **No external dependencies**: Reduces load time and complexity

## Security Considerations

- **Sandbox isolation**: Taskpane runs in iframe sandbox
- **Content Security Policy**: Office.js enforces CSP
- **No eval()**: All code is static
- **HTML sanitization**: Content is rendered as-is (user responsibility)

## Deployment Architecture

```
GitHub Repository
    ↓
GitHub Pages (Static Hosting)
    ↓
manifest.xml (points to hosted taskpane.html)
    ↓
User sideloads manifest.xml in Outlook
    ↓
Outlook loads taskpane.html from GitHub Pages
```

## Limitations & Constraints

1. **Single-file design**: No build step, no bundling
2. **No backend**: All data stored in email custom properties
3. **Office.js only**: Limited to Office API capabilities
4. **Static hosting**: No server-side logic or database
5. **Sideload only**: Not available in Office Store
6. **Manifest versioning**: Manual version updates required

## Future Architecture Considerations

### Potential Enhancements

1. **Build Pipeline**: Webpack/Vite for bundling and optimization
2. **Backend Service**: API for AI summarization or data persistence
3. **Component Framework**: React/Vue for complex UI
4. **Testing Framework**: Jest/Vitest for automated testing
5. **CI/CD Pipeline**: GitHub Actions for automated deployment

### Scalability

Current architecture is suitable for:
- Single-file, lightweight add-in
- Static hosting
- Manual sideloading

For larger projects, consider:
- Modular architecture with build step
- Backend service for complex logic
- Automated testing and deployment
- Office Store distribution

## References

- [Office Add-ins Architecture](https://learn.microsoft.com/en-us/office/dev/add-ins/overview/office-add-ins)
- [Outlook Add-in API](https://learn.microsoft.com/en-us/javascript/api/outlook)
- [Custom Properties](https://learn.microsoft.com/en-us/office/dev/add-ins/outlook/metadata-for-an-outlook-add-in)
- [Taskpane Design](https://learn.microsoft.com/en-us/office/dev/add-ins/design/task-pane-add-ins)
