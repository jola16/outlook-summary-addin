# Outlook Summary Add-in

A Microsoft Office add-in for Outlook that displays summaries and actionable items for email conversations directly in the Outlook taskpane.

## Features

- **Markdown to HTML Rendering**: Automatically converts markdown-formatted content to HTML with fallback to raw values
- **Custom Properties Storage**: Reads summary and actions data from email metadata
- **Bilingual Support**: Automatically detects and displays content in Swedish or English
- **XSS Protection**: All HTML is sanitized with DOMPurify before rendering
- **Responsive Design**: Adapts to different taskpane widths
- **Error Resilience**: Gracefully handles markdown conversion failures

## Installation

### Prerequisites

- Microsoft Outlook (desktop or web)
- Access to sideload add-ins in your Outlook environment

### Steps

1. Clone or download this repository
2. Host the `src/taskpane/taskpane.html` file on a web server (e.g., GitHub Pages)
3. Update the `SourceLocation` URLs in `manifest.xml` to point to your hosted file
4. Sideload the `manifest.xml` file in Outlook:
   - **Outlook Desktop**: File → Options → Trust Center → Trust Center Settings → Trusted Add-in Catalogs
   - **Outlook Web**: Go to https://aka.ms/olksideload and upload the manifest.xml file

## Usage

1. Open an email message in Outlook
2. Click the "Visa sammanfattning" (Show Summary) button in the ribbon
3. The taskpane opens showing the email's summary and actions
4. Switch between tabs using the "Åtgärder" (Actions) and "Sammanfattning" (Summary) buttons

## Project Structure

```
outlook-summary-addin/
├── manifest.xml              # Office add-in configuration and metadata
├── src/
│   └── taskpane/
│       └── taskpane.html     # Main UI, styles, and JavaScript logic
├── AGENTS.md                 # Agent guidelines for development
├── README.md                 # This file
└── CHANGELOG.md              # Version history and changes
```

## Development

### Architecture

The add-in is built as a single-file application:
- **HTML**: Semantic structure with header, content area, and status bar
- **CSS**: Segoe UI design system with responsive layout
- **JavaScript**: Vanilla JS using Office.js API for Outlook integration

### Key Components

- **Header**: Displays sender, recipient count, and subject
- **Tabs**: Navigation between Actions and Summary views
- **Content Area**: Scrollable pane for displaying HTML content
- **Status Bar**: Shows loading, saving, error, and success messages

### Localization

Strings are managed in the `t` object in `taskpane.html`:

```javascript
const t = {
  tabActions: isSv ? "Åtgärder" : "Actions",
  tabSummary: isSv ? "Sammanfattning" : "Summary",
  // ... more strings
};
```

Language detection uses `navigator.language`:
```javascript
const isSv = navigator.language.toLowerCase().startsWith("sv");
```

### Custom Properties

The add-in reads data from email custom properties:
- `summary`: Markdown or HTML content for the Summary section
- `actions`: Markdown or HTML content for the Actions section

Content is expected in markdown format. If markdown parsing fails, the raw value is displayed.

Access via Office.js:
```javascript
item.loadCustomPropertiesAsync((result) => {
  const props = result.value;
  const summary = props.get("summary");
  const actions = props.get("actions");
});
```

**Note**: The add-in is read-only and does not persist data back to custom properties.

## Testing

Before committing changes, verify:

- [ ] Add-in loads without console errors
- [ ] Both Swedish and English UI strings display correctly
- [ ] Markdown content is correctly converted to HTML
- [ ] HTML content is sanitized and rendered safely
- [ ] Markdown conversion failures fall back to raw values gracefully
- [ ] Custom properties load correctly
- [ ] Error scenarios are handled gracefully
- [ ] Layout is responsive at different pane widths
- [ ] Tested in both Outlook desktop and web

## Deployment

1. Update version number in `manifest.xml`
2. Ensure `src/taskpane/taskpane.html` is hosted and accessible
3. Update `SourceLocation` URLs in `manifest.xml` if needed
4. Commit changes with appropriate message
5. Users can sideload the updated `manifest.xml`

## Known Limitations

- Single-file architecture (no build step or bundling)
- No backend; all data stored in email custom properties
- Limited to Office.js capabilities and Outlook permissions
- Requires manual sideloading (not available in Office Store)

## Support

For issues, questions, or contributions, please refer to the project repository.

## License

See LICENSE file for details.

## References

- [Office Add-ins Documentation](https://learn.microsoft.com/en-us/office/dev/add-ins/)
- [Office JavaScript API](https://learn.microsoft.com/en-us/javascript/api/office)
- [Outlook Add-in API](https://learn.microsoft.com/en-us/javascript/api/outlook)
- [Custom Properties in Office Add-ins](https://learn.microsoft.com/en-us/office/dev/add-ins/outlook/metadata-for-an-outlook-add-in)
