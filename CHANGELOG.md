# Changelog

All notable changes to the Outlook Summary Add-in project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
