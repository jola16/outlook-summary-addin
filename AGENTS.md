# AGENTS.md – Outlook Summary Add-in

## Project Overview

**Outlook Summary Add-in** is a Microsoft Office add-in for Outlook that displays summaries and actions for selected email conversations. The add-in is built as a web-based taskpane that integrates with Outlook's mail reading interface.

### Technology Stack

- **Frontend**: HTML5, CSS3, vanilla JavaScript
- **Office Integration**: Office JavaScript API (Office.js)
- **Configuration**: XML manifest (Office add-in format)
- **Deployment**: Static hosting (GitHub Pages)
- **Localization**: Swedish (sv-SE) and English (en) support

### Project Structure

```
outlook-summary-addin/
├── manifest.xml              # Office add-in configuration
├── src/
│   └── taskpane/
│       └── taskpane.html     # Main UI and logic (HTML + CSS + JS)
└── .roo/                     # Agent rules and guidelines
```

## Project Characteristics

### What This Project Does

1. **Taskpane UI**: Displays a sidebar in Outlook when reading an email message
2. **Vertical Layout**: Shows Summary and Actions sections stacked vertically (no tabs)
3. **Markdown Rendering**: Reads markdown-formatted content from email custom properties and converts to HTML
4. **Read-Only Design**: Loads data from email custom properties; does NOT write back
5. **Bilingual Support**: Automatically detects user language (Swedish/English)

### Key Features

- Responsive taskpane with header, content area, and status bar
- Markdown-to-HTML conversion with DOMPurify sanitization
- Graceful error handling with fallback to raw values if markdown parsing fails
- XSS protection via DOMPurify sanitization of all HTML
- Automatic language detection based on browser locale
- Local icon assets (16x16, 32x32, 80x80) served from GitHub Pages

## Agent Guidelines

### Code Style & Standards

- **Language**: Use English for all code comments, documentation, and commit messages
- **Localization**: Maintain Swedish and English translations in the `t` object
- **Formatting**: Follow Segoe UI design system (colors, spacing, typography)
- **Accessibility**: Ensure semantic HTML and keyboard navigation

### File Editing Workflow

When modifying files:

1. Use `apply_diff` tool for targeted changes
2. If diff fails, re-read the relevant section and recalculate
3. If still failing, re-read the entire file and use `write_to_file`

### Development Approach

- **Minimal Changes**: Keep modifications small and coherent
- **Pattern Consistency**: Follow existing code patterns (e.g., i18n structure, event handling)
- **No Refactoring Without Reason**: Only refactor when necessary for the task
- **Testing**: Manually test in Outlook after changes to taskpane.html

### Linting & Formatting

This project does not currently use automated linting tools (no Python, no Node.js build pipeline). However:

- **HTML**: Keep semantic and valid
- **CSS**: Follow existing style organization (header, content, status, loading sections)
- **JavaScript**: Use vanilla JS; avoid external dependencies unless necessary

### Definition of Done (DoD) for This Project

**Important**: This is an HTML/CSS/JavaScript Office Add-in, NOT a Python project. The generic DoD checklist in `.roo/rules/general.md` is Python-focused. For this project, follow this adapted DoD process:

1. **Code Review** – Manual review of HTML, CSS, and JavaScript changes:
   - Verify HTML is semantic and valid (no console errors in browser)
   - Check CSS follows existing style patterns (colors, spacing, typography)
   - Ensure JavaScript is readable and follows existing patterns (vanilla JS, no external deps unless approved)
   - No linting/formatting tools are used (no ruff, pylint, prettier)

2. **Documentation** – Update relevant documentation:
   - Update `AGENTS.md` if project scope or structure changes
   - Add comments in `taskpane.html` for new features or complex logic
   - Update `README.md` if public-facing behavior changed
   - Keep `manifest.xml` descriptions accurate and localized

3. **Versioning** – If the change is non-trivial:
   - Bump version in `CHANGELOG.md` with a summary of what changed
   - Sync version to `manifest.xml` `<Version>` tag and `SourceLocation` URL (with cache-busting `?v=X.Y.Z`)
   - Update `VERSION` constant in `src/taskpane/taskpane.html`

4. **Manual Testing** – Before committing:
   - [ ] Test in Outlook (desktop or web)
   - [ ] Verify both Swedish and English UI strings
   - [ ] Check markdown conversion (test with markdown and HTML content)
   - [ ] Verify HTML is sanitized and XSS-safe
   - [ ] Test custom properties loading (read-only)
   - [ ] Test error scenarios (network, permissions, markdown parsing failures)
   - [ ] Validate HTML structure (no console errors)
   - [ ] Check responsive layout at different pane widths
   - [ ] Verify icons load correctly from resources/

### Documentation

- Update this file (`AGENTS.md`) if project scope or structure changes
- Keep `manifest.xml` descriptions accurate and localized
- Document any new features in comments within `taskpane.html`

### Commit Messages

Use English perfect tense without the word "has":

- ✅ "Updated taskpane styling for better readability"
- ✅ "Added error handling for custom properties"
- ❌ "Update taskpane" (imperative)
- ❌ "Has updated taskpane" (contains "has")

### Common Tasks

#### Adding a New Section

1. Add section div to content area (`#pane-<name>`)
2. Add i18n string to `t` object
3. Update `showContent()` function to populate the section
4. Test in Outlook

#### Modifying Markdown Conversion

1. Edit the `marked.parse()` call in `showContent()`
2. Ensure try-catch wraps conversion with fallback to raw value
3. Always sanitize output with `DOMPurify.sanitize()`
4. Test with various markdown formats and edge cases

#### Modifying Styling

1. Edit CSS in `<style>` block
2. Follow existing color scheme and spacing
3. Test responsive behavior
4. Verify in both Swedish and English locales

#### Updating Localization

1. Add/modify strings in the `t` object
2. Provide both Swedish and English versions
3. Use `isSv` variable for language detection
4. Test with browser language settings

#### Handling Custom Properties (Read-Only)

1. Use `item.loadCustomPropertiesAsync()` to load
2. Use `props.get()` for read-only access
3. Never use `props.set()` or `props.saveAsync()` (add-in is read-only)
4. Always handle async results with proper status messages

#### Syncing Version from CHANGELOG

After DoD checklist updates `CHANGELOG.md` with new version:

1. **Sync version to `manifest.xml`** – Update `<Version>` tag to match CHANGELOG
2. **Add cache-busting query parameter** – Update `SourceLocation` URLs in `manifest.xml` to include version:
   ```xml
   <SourceLocation DefaultValue="https://jola16.github.io/outlook-summary-addin/src/taskpane/taskpane.html?v=1.0.3.0" />
   ```
3. **Update version in taskpane footer** – Update `VERSION` constant in `src/taskpane/taskpane.html`:
   ```javascript
   const VERSION = "1.0.3.0";
   ```

**Important**: The version must be synchronized across three places:
- `CHANGELOG.md` (updated by DoD checklist)
- `manifest.xml` `<Version>` tag and `SourceLocation` query parameter
- `src/taskpane/taskpane.html` `VERSION` constant (displayed in footer)

**Cache-Busting Strategy**: Adding `?v=X.Y.Z` to the `SourceLocation` URL forces Outlook to bypass its cache and load the new taskpane.html immediately, rather than waiting for cache expiration. This ensures users get the latest version without delay.

**Workflow Rule**: Do NOT commit `manifest.xml` separately. It should always be commited together with `CHANGELOG.md` in the same commit when the user runs the `/commit-checklist` command. This ensures version synchronization and maintains a clean commit history.

Example:
```xml
<!-- manifest.xml -->
<Version>1.0.3.0</Version>
<SourceLocation DefaultValue="https://jola16.github.io/outlook-summary-addin/src/taskpane/taskpane.html?v=1.0.3.0" />
```

```javascript
// src/taskpane/taskpane.html
const VERSION = "1.0.3.0";
```

```markdown
<!-- CHANGELOG.md (updated by DoD checklist) -->
## [1.0.3.0] - 2026-03-12
```

## Known Limitations & Considerations

- **Single File Architecture**: All logic is in `taskpane.html` (no build step)
- **No External Dependencies**: Relies only on Office.js and browser APIs
- **Static Hosting**: Deployed to GitHub Pages; no backend
- **Office API Constraints**: Limited to Office.js capabilities and permissions
- **Manifest Versioning**: Version in `manifest.xml` must be updated for deployments

## Testing Checklist

Before committing changes:

- [ ] Test in Outlook (desktop or web)
- [ ] Verify both Swedish and English UI strings
- [ ] Check tab switching functionality
- [ ] Confirm custom properties save/load
- [ ] Test error scenarios (network, permissions)
- [ ] Validate HTML structure (no console errors)
- [ ] Check responsive layout at different pane widths

## References

- [Office Add-ins Documentation](https://learn.microsoft.com/en-us/office/dev/add-ins/)
- [Office JavaScript API](https://learn.microsoft.com/en-us/javascript/api/office)
- [Outlook Add-in API](https://learn.microsoft.com/en-us/javascript/api/outlook)
- [Custom Properties in Office Add-ins](https://learn.microsoft.com/en-us/office/dev/add-ins/outlook/metadata-for-an-outlook-add-in)
