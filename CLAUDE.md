# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

**Outlook Summary Add-in** is a single-file Office add-in: the entire application is `src/taskpane/taskpane.html` (HTML + CSS + JS combined). It displays email summaries and actions by reading custom properties from the selected email, converting markdown to HTML, and rendering with DOMPurify sanitization.

### Key Architectural Concepts

1. **Single-File Application**: No build step. The taskpane.html file is served directly via GitHub Pages. Changes to this file are immediately reflected on deployment.

2. **Read-Only Design**: The add-in **reads only** from email custom properties (`summary`, `actions`). It does NOT write back to custom properties.

3. **Markdown Conversion Pipeline**:
   - Expect content in email custom properties as **markdown format**
   - Use `marked.parse()` (CDN, v11.1.1) to convert markdown → HTML
   - Wrap conversion in try-catch: on parsing error, fall back to raw value
   - Sanitize all HTML output with `DOMPurify.sanitize()` (CDN, v3.0.8) before rendering
   - Never attempt format detection; always attempt markdown parsing

4. **Bilingual UI**: Language detection via `navigator.language`. Strings are in the `t` object. Always provide both Swedish and English strings in the format:
   ```javascript
   key: isSv ? "Swedish text" : "English text"
   ```

5. **Manifest Versioning**: When bumping version, update **all three** locations:
   - `manifest.xml` → `<Version>` tag
   - `src/taskpane/taskpane.html` → `const VERSION = "..."`
   - `manifest.xml` → All `?v=X.X.X` query parameters in URLs

## Development Workflow

### No Build, Lint, or Test Commands

This project has no build step, no linter, and no automated tests currently. Changes to the HTML file are served directly from GitHub Pages.

### Local Testing

- Sideload `manifest.xml` in Outlook (desktop or web)
- Open an email and verify the taskpane loads and displays correctly
- Check browser console (F12) for JavaScript errors
- Test markdown conversion: add markdown content to email custom properties and verify it renders as HTML
- Test bilingual UI by changing browser language

### Icon Assets

Icons are stored in `resources/` and referenced in `manifest.xml`. Three sizes are required:
- `short_summary_16.png` – ribbon button (normal DPI)
- `short_summary_32.png` – ribbon button (high DPI)
- `short_summary_80.png` – high-resolution display

Ensure icons are included in GitHub Pages deployment.

## Versioning Strategy

Use semantic versioning: `MAJOR.MINOR.PATCH`

**Before bumping:**
- Ask the user which bump type (PATCH, MINOR, MAJOR) unless they explicitly specify
- PATCH: bug fixes, minor improvements
- MINOR: new features
- MAJOR: breaking changes

**When bumping:**
1. Update `<Version>` tag in `manifest.xml`
2. Update `const VERSION` in `src/taskpane/taskpane.html`
3. Update all `?v=X.X.X` query parameters in `manifest.xml` (SourceLocation and Urls sections)
4. Update CHANGELOG.md with a new section for the version
5. Generate a descriptive commit message and ask: "Shall we commit?"
6. After commit, ask: "Shall we push?"

## Deployment

The add-in is deployed via GitHub Pages at `https://jola16.github.io/outlook-summary-addin/`

- The static site serves `src/taskpane/taskpane.html` and `resources/` files
- Version query params in manifest.xml ensure Outlook picks up updates (e.g., `?v=1.4.9`)
- No build or release process needed; commits to `master` are automatically live

## Office Add-in Configuration

The `manifest.xml` file defines:
- Ribbon button configuration (label, icon, tooltip in Swedish/English)
- Taskpane source location (points to GitHub Pages)
- Custom property permissions (ReadWriteItem)
- Version overrides for backward compatibility (V1_0 and V1_1)

**Do not modify** ribbon configuration without understanding how Office picks up changes (changes require version bump).
