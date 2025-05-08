# Slack Token Extractor

Extract your Slack XOXC and XOXD tokens easily using browser extensions or Selenium automation.

## Project Structure

- [`chrome/`](chrome/) — Chrome/Chromium extension
- [`firefox/`](firefox/) — Firefox add-on
- Selenium script (see below)

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

You can also extract tokens using a Python Selenium script. This is useful for automation or if you prefer not to use a browser extension.

### Prerequisites
- Python 3.8+
- [Selenium](https://pypi.org/project/selenium/)
- [geckodriver](https://github.com/mozilla/geckodriver/releases) (for Firefox) or [chromedriver](https://chromedriver.chromium.org/) (for Chrome)

### Usage
1. Clone this repository:
   ```sh
   git clone https://github.com/maorfr/slack-token-extractor.git
   cd slack-token-extractor
   ```
2. Install dependencies:
   ```sh
   pip install selenium
   ```
3. Run the script (example for Firefox):
   ```sh
   python run.py
   ```
   - The script will open a browser window. Log in to Slack if prompted.
   - Follow the instructions in the terminal to extract your tokens.
   - Tokens will be displayed and you can optionally save them to a `.env` file.

**Note:**
- The script uses a persistent browser profile so you only need to log in once.
- You can adapt the script to use Chrome by changing the driver initialization.

---

## Security
- Tokens are only stored locally and are never transmitted anywhere.
- **Never share your tokens.**

---

## License
MIT 