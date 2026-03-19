# Changelog

All notable changes to the Outlook Summary Add-in project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.8] - 2026-03-19

### Added
- Markdown-to-HTML conversion in taskpane: content is automatically detected as markdown or HTML
- DOMPurify sanitization for XSS protection: all HTML is sanitized before rendering to prevent injection attacks
- Markdown format detection with support for headers, bold, italic, lists, links, and inline code
- CDN dependencies: marked.js (v11.1.1) for markdown parsing, DOMPurify (v3.0.8) for HTML sanitization

### Changed
- Modified `showContent()` function to support both markdown and HTML rendering
- Added `isMarkdown()` detection function to distinguish between markdown and HTML content
- Sanitization is applied to all content before rendering, preserving all safe HTML formatting

## [1.4.7] - 2026-03-13

### Fixed
- Fixed fallback data handling: only set fallback summary/actions if property is missing (undefined), not if empty string
- Empty string values are now preserved instead of being overwritten with fallback text

### Changed
- Converted tab-based layout to vertical stacked layout for Summary and Actions
- Summary now displays first, followed by Actions, both visible simultaneously
- Removed tab navigation buttons from header
- Removed pin button and legacy pin functionality (now using Outlook's built-in pinning)
- Updated subject header to support word-break instead of text-overflow ellipsis
- Set subject header min-height to two line heights to prevent layout shift

### Added
- Settings section placeholder for future configuration options
- Section titles with uppercase styling for better visual hierarchy

## [1.4.6] - 2026-03-13

### Changed
- Converted tab-based layout to vertical stacked layout for Summary and Actions
- Summary now displays first, followed by Actions, both visible simultaneously
- Removed tab navigation buttons from header
- Removed pin button and legacy pin functionality (now using Outlook's built-in pinning)
- Updated subject header to support word-break instead of text-overflow ellipsis
- Set subject header min-height to two line heights to prevent layout shift

### Added
- Settings section placeholder for future configuration options
- Section titles with uppercase styling for better visual hierarchy

## [1.4.5] - 2026-03-13

### Added
- Debug script `debug/read_user_properties.py` for reading Office.js customProperties via win32com MAPI
- Debug tool `debug/read_custom_properties.html` for reading customProperties from Outlook UI
- Plan document `plans/2026-03-13 Hur man läser CustomProperties enligt Perplexity.md` with MAPI property format documentation

### Documentation
- Documented correct MAPI extended property format for customProperties access
- Added usage instructions for both debug tools (Python script and HTML/Office.js tool)

## [1.4.4] - 2026-03-13

### Added
- ItemChanged event handler for pinned taskpane support
- updateUIForCurrentItem() function to handle both initial load and item changes

### Changed
- Refactored Office.onReady to use updateUIForCurrentItem()
- Registered ItemChanged event on mailbox level (not item level) for proper pinned taskpane behavior
- UI now updates when user switches between emails while taskpane is pinned

## [1.4.3] - 2026-03-12

### Changed
- Updated VersionOverrides to 1.1 (required for SupportsPinning support)
- Bumped version to 1.4.3 to ensure Outlook picks up VersionOverrides 1.1 configuration
- Added dual VersionOverrides support (1.0 for backward compatibility, 1.1 for SupportsPinning)

## [1.4.2] - 2026-03-12

### Added
- SupportsPinning attribute in manifest.xml to enable taskpane pinning in Outlook

### Changed
- Bumped version to 1.4.2 to ensure Outlook picks up SupportsPinning configuration

## [1.4.1] - 2026-03-12

### Added
- SVG pin button with visual feedback (dark green #107c10 for pinned, light green for unpinned)
- Status message when data is loaded from customProperties
- i18n strings for pin/unpin actions (Swedish: "Fäst taskpane" / "Lossa taskpane")

### Changed
- Replaced emoji pin button with SVG icon for better visual consistency
- Modified togglePin() function to change SVG color using CSS color-mix (with opacity 0.35 fallback for older browsers)

## [1.4.0] - 2026-03-12

### Added
- Hardcoded version display in taskpane footer
- Pin button (📌) to pin/unpin taskpane in Outlook

### Changed
- Updated versioning rules: minor changes now bump patch version (e.g., 1.2.1 → 1.2.2)
- Updated `.roo/rules/general.md` to reflect new versioning strategy

## [1.3.0] - 2026-03-12

### Added
- Version footer in taskpane that displays add-in version from URL query parameter
- Users can now see which version of the add-in is installed

## [1.0.2.0] - 2026-03-12

### Added
- Comprehensive project documentation suite:
  - AGENTS.md with agent guidelines and development standards
  - README.md with installation, usage, and development instructions
  - CHANGELOG.md with version history and semantic versioning
  - docs/architecture.md with detailed system architecture documentation
- Project structure with subdirectories:
  - docs/ for architecture and technical documentation
  - tests/ for test files (future)
  - experiments/ for experimental code (future)
  - debug/ for debug scripts (future)
- Architecture documentation covering:
  - System architecture diagrams
  - Component architecture (HTML, CSS, JavaScript)
  - Data flow and custom properties schema
  - Error handling and performance considerations
  - Security considerations and deployment architecture
  - Future enhancement recommendations

### Documentation
- Documented all UI strings and localization approach
- Documented custom properties schema and namespace
- Documented error handling strategy
- Documented deployment process and limitations

## [1.0.1.0] - 2026-03-12

### Added
- Initial project documentation (AGENTS.md, README.md, CHANGELOG.md)
- Comprehensive agent guidelines for development and maintenance
- Testing checklist for quality assurance

### Fixed
- Improved error handling for custom properties loading
- Enhanced status messages for user feedback

### Changed
- Updated manifest version to 1.0.1.0

## [1.0.0.0] - 2026-01-01

### Added
- Initial release of Outlook Summary Add-in
- Dual-tab interface (Actions and Summary)
- Custom properties storage for email metadata
- Bilingual support (Swedish and English)
- Responsive taskpane design
- Status indicators for loading, saving, and error states
- Fallback content for emails without custom properties
- Office.js integration for Outlook API access
- Segoe UI design system styling

### Features
- Display email sender, recipient count, and subject in header
- Tab-based navigation between Actions and Summary views
- Automatic language detection based on browser locale
- Graceful error handling with user-facing messages
- Persistent data storage via email custom properties
- Sample data generation for demonstration purposes

### Technical Details
- Single-file architecture (taskpane.html)
- Vanilla JavaScript (no external dependencies except Office.js)
- Semantic HTML5 structure
- CSS3 with flexbox layout
- Static hosting on GitHub Pages
- XML manifest for Office add-in configuration

---

## Version History

### Versioning Scheme

This project uses semantic versioning with the format: `MAJOR.MINOR.PATCH.BUILD`

- **MAJOR**: Significant feature additions or breaking changes
- **MINOR**: New features or enhancements
- **PATCH**: Bug fixes and minor improvements
- **BUILD**: Internal build number

### Future Enhancements

Potential improvements for future releases:

- [ ] Support for additional email properties (attachments, dates)
- [ ] Rich text editor for actions and summary
- [ ] Integration with external services (AI summarization)
- [ ] Keyboard shortcuts for tab navigation
- [ ] Dark mode support
- [ ] Additional language support (German, French, etc.)
- [ ] Performance optimizations for large conversations
- [ ] Accessibility improvements (ARIA labels, screen reader support)
