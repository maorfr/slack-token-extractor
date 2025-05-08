from selenium import webdriver
import json
import re

# Setup FirefoxDriver
firefox_options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=firefox_options)

try:
    print("Opening Slack login page...")
    driver.get("https://app.slack.com/client/")  # or your workspace URL

    input("➡️  Please log in to Slack in the browser window that opened. Press ENTER when ready...")

    print("Fetching localStorage.localConfig_v2...")
    local_config_json = driver.execute_script("return localStorage.localConfig_v2")

    if not local_config_json:
        print("❌ Could not find localConfig_v2 in localStorage. Is Slack loaded?")
        driver.quit()
        exit(1)

    local_config = json.loads(local_config_json)

    print("Extracting team ID from current URL...")
    current_path = driver.execute_script("return window.location.pathname")
    team_id_match = re.match(r"^/client/([A-Z0-9]+)", current_path)

    if not team_id_match:
        print("❌ Could not extract team ID from the current path.")
        driver.quit()
        exit(1)

    team_id = team_id_match.group(1)

    print(f"Found team ID: {team_id}")

    xoxc_token = local_config['teams'][team_id]['token']

    print(f"✅ SLACK_MCP_XOXC_TOKEN: {xoxc_token}")

    print("Fetching 'd' cookie (XOXD token)...")
    cookies = driver.get_cookies()
    d_cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == 'd'), None)

    if not d_cookie:
        print("❌ 'd' cookie not found.")
        driver.quit()
        exit(1)

    print(f"✅ SLACK_MCP_XOXD_TOKEN: {d_cookie}")

    save_choice = input("Would you like to save these to a .env file? (y/n): ").lower()
    if save_choice == 'y':
        with open(".slack_tokens.env", "w") as env_file:
            env_file.write(f"SLACK_MCP_XOXC_TOKEN={xoxc_token}\n")
            env_file.write(f"SLACK_MCP_XOXD_TOKEN={d_cookie}\n")
        print("✅ Tokens saved to .slack_tokens.env")

finally:
    driver.quit()

print("🎉 Done!")
