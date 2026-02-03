# Slack Token Extractor

Extract your Slack XOXC and XOXD tokens easily using browser extensions or Python automation.

## Why?

Slack's official API requires workspace admin approval for most useful scopes. These tokens let you access Slack programmatically using your own user permissions — no admin approval needed.

**Common use cases:**
- Use with [slack-mcp-server](https://github.com/korotovsky/slack-mcp-server) for AI assistant integration
- Personal automation scripts
- Backup your own messages
- Research and analysis

## Extraction Methods

| Method | Best For | Requires |
|--------|----------|----------|
| [Playwright](#4-playwright-script-recommended) | Automation, CI/CD | Python 3.8+ |
| [Selenium](#3-selenium-script) | Legacy setups | Python 3.8+, chromedriver |
| [Chrome Extension](#1-chrome-extension) | Quick one-time extraction | Chrome browser |
| [Firefox Add-on](#2-firefox-add-on) | Quick one-time extraction | Firefox browser |

---

## 1. Chrome Extension

See [`chrome/README.md`](chrome/README.md) for full instructions.

**Quick Start:**
1. Go to `chrome://extensions` in Chrome
2. Enable Developer mode
3. Click "Load unpacked" and select the `chrome` directory
4. Visit your Slack workspace and click the extension icon to view your tokens

---

## 2. Firefox Add-on

See [`firefox/README.md`](firefox/README.md) for full instructions.

**Quick Start:**
1. Go to `about:debugging#/runtime/this-firefox` in Firefox
2. Click "Load Temporary Add-on..." and select the `manifest.json` file in the `firefox` directory
3. Visit your Slack workspace and click the extension icon to view your tokens

---

## 3. Selenium Script

Extract tokens using Python + Selenium. Useful if you already have Selenium set up.

### Prerequisites
- Python 3.8+
- [Selenium](https://pypi.org/project/selenium/)
- [chromedriver](https://chromedriver.chromium.org/) or [geckodriver](https://github.com/mozilla/geckodriver/releases)

### Usage
```sh
pip install selenium
python chrome.py   # For Chrome
python firefox.py  # For Firefox
```

The script will open a browser window. Log in to Slack if prompted, then follow the terminal instructions.

---

## 4. Playwright Script (Recommended)

Modern alternative to Selenium with better performance, reliability, and no external driver required.

### Prerequisites
- Python 3.8+

### Installation
```sh
pip install playwright
playwright install chromium
```

### Usage

**Interactive mode** (opens browser window):
```sh
python playwright_extract.py
```

**Headless mode** (reuses existing session):
```sh
python playwright_extract.py --headless
```

**Specific workspace**:
```sh
python playwright_extract.py --workspace https://mycompany.slack.com
```

**Custom output file**:
```sh
python playwright_extract.py --output ~/.config/slack/tokens.env
```

### Features
- **Persistent profile**: Log in once, reuse session for future extractions
- **Headless support**: Run without GUI after initial login
- **Multiple workspaces**: Extract from any workspace you have access to
- **Secure output**: Tokens saved with `600` permissions

### Options
```
--workspace, -w   Slack workspace URL (default: app.slack.com)
--headless        Run without browser window (needs prior login)
--output, -o      Output file path (default: .slack_tokens.env)
--profile-dir     Browser profile directory for session persistence
--no-save         Don't prompt to save tokens
```

---

## Using Your Tokens

### With slack-mcp-server

The extracted tokens work directly with [slack-mcp-server](https://github.com/korotovsky/slack-mcp-server):

```sh
export SLACK_MCP_XOXC_TOKEN="xoxc-..."
export SLACK_MCP_XOXD_TOKEN="xoxd-..."
```

Or source the generated `.env` file:
```sh
source .slack_tokens.env
```

### With curl

```sh
curl -H "Authorization: Bearer $SLACK_MCP_XOXC_TOKEN" \
     -H "Cookie: d=$SLACK_MCP_XOXD_TOKEN" \
     "https://slack.com/api/conversations.list"
```

---

## Token Lifetime

- Tokens remain valid as long as your browser session is active
- Typically lasts weeks to months with regular Slack usage
- Invalidated by: logging out, password change, or admin session revocation
- Re-run the extractor when tokens expire

---

## Security

- Tokens are stored **locally only** and never transmitted anywhere
- Output files are created with `600` permissions (owner read/write only)
- **Never share your tokens** — they provide full access to your Slack account
- **Never commit tokens to git** — add `.slack_tokens.env` to `.gitignore`

---

## Troubleshooting

**"Could not find XOXC token"**
- Make sure you're fully logged into Slack
- Wait for the workspace to fully load before pressing Enter
- Try a different extraction method

**"Not logged in and running in headless mode"**
- Run once without `--headless` to log in
- Your session will be saved for future headless runs

**Tokens stopped working**
- Your session expired — re-run the extractor
- Check if you were logged out of Slack

---

## Appreciation

Special thanks to [@korotovsky](https://github.com/korotovsky) for the excellent [slack-mcp-server](https://github.com/korotovsky/slack-mcp-server). The clear documentation made it much easier to understand and work with Slack tokens.

---

## License

MIT
