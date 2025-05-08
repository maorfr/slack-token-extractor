# Slack Token Extractor (Chrome Extension)

This Chrome extension extracts Slack tokens (XOXC and XOXD) from your Slack workspace.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/maorfr/slack-token-extractor.git
   cd slack-token-extractor/chrome
   ```
2. **Open Chrome and go to** `chrome://extensions`
3. **Enable Developer mode** (toggle in the top right)
4. **Click "Load unpacked"** and select the `chrome` directory from this repository
5. **Visit your Slack workspace** (e.g., `https://your-workspace.slack.com`)
6. **Click the extension icon** in the Chrome toolbar to view your tokens

## How it works
- The extension reads your Slack `localStorage` and cookies to extract the XOXC and XOXD tokens.
- Tokens are displayed in the popup when you click the extension icon.

## Security
- Tokens are only stored locally in your browser's extension storage.
- **Never share your tokens.**

## Troubleshooting
- If you don't see the extension icon, make sure it's pinned in the Chrome toolbar.
- If tokens do not appear, ensure you are logged in to Slack and have visited your workspace in the current tab.

---
[Back to main repo](https://github.com/maorfr/slack-token-extractor) 