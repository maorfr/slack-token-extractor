# Slack Token Extractor (Firefox Add-on)

This Firefox add-on extracts Slack tokens (XOXC and XOXD) from your Slack workspace.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/maorfr/slack-token-extractor.git
   cd slack-token-extractor/firefox
   ```
2. **Open Firefox and go to** `about:debugging#/runtime/this-firefox`
3. **Click "Load Temporary Add-on..."**
4. **Select the `manifest.json` file** in the `firefox` directory
5. **Visit your Slack workspace** (e.g., `https://your-workspace.slack.com`)
6. **Click the extension icon** in the Firefox toolbar to view your tokens

## How it works
- The add-on reads your Slack `localStorage` and cookies to extract the XOXC and XOXD tokens.
- Tokens are displayed in the popup when you click the extension icon.

## Security
- Tokens are only stored locally in your browser's extension storage.
- **Never share your tokens.**

## Troubleshooting
- If you don't see the extension icon, check the Extensions (puzzle piece) menu and pin it to the toolbar.
- If tokens do not appear, ensure you are logged in to Slack and have visited your workspace in the current tab.
- If you see errors about `background.service_worker`, make sure you are using the Manifest V2 version (as provided here).

---
[Back to main repo](https://github.com/maorfr/slack-token-extractor) 