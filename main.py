import requests
import time
import json
import os

CONFIGFILE = "config.json"
with open(CONFIGFILE, 'r') as f:
    config = json.load(f)

# headers not ud  :rofl:
HEADERS = {
    "authorization": config["token"],
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "x-discord-locale": "en-US",
    "x-discord-timezone": "Europe/London"
}


def loadConfig():
    defaultSettings = {
        "token": "ur account token",
        "monitorURL": "url to watch (webhook link)",
        "createURL": "url to create new webhook (https://discord.com/api/v9/webhooks/{channel id}/webhooks)",
        "checkInterval": 1
    }

    if os.path.exists(CONFIGFILE):
        try:
            with open(CONFIGFILE, 'r') as f:
                config = json.load(f)
                for key, value in defaultSettings.items():
                    if key not in config:
                        config[key] = value
                return config
        except Exception as e:
            print(f"failed to load config: {e}")

    print("error: config file not found. please create config.json with required settings")
    saveConfig(defaultSettings)
    return defaultSettings


def saveConfig(config):
    try:
        with open(CONFIGFILE, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"config saved.")
    except Exception as e:
        print(f"failed to save config: {e}")


def checkExists(url, token):
    try:
        headers = HEADERS.copy()
        headers["authorization"] = token
        response = requests.get(url, headers=headers, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"failed to get: {e}")
        return False


def sendCreate(webhookURL, message, token, config):
    try:
        payload = {
            "name": "AutoHook"
        }
        headers = HEADERS.copy()
        headers["authorization"] = token
        response = requests.post(webhookURL, json=payload, headers=headers, timeout=5)
        print(f"status: {response.status_code}")

        if response.status_code == 200:
            webhookData = response.json()
            if 'url' in webhookData:
                newWebhook = webhookData['url']
                print(f"new webhook created: {newWebhook}")
                config['monitorURL'] = newWebhook
                saveConfig(config)
                return newWebhook
        return None
    except requests.exceptions.RequestException as e:
        print(f"failed to post: {e}")
        return None


def main():
    print("starting autohook.")

    config = loadConfig()

    if not config['token'] or not config['monitorURL'] or not config['createURL']:
        print("error: please set token, monitorURL, and createURL in config.json")
        return

    monitorURL = config['monitorURL']
    token = config['token']
    createURL = config['createURL']
    checkInterval = config['checkInterval']

    print(f"monitoring: {monitorURL}")

    urlFound = True

    try:
        while True:
            urlExists = checkExists(monitorURL, token)

            if urlExists:
                if not urlFound:
                    print(f"[{time.strftime('%H:%M:%S')}] webhook is back online.")
                urlFound = True
            else:
                print(f"[{time.strftime('%H:%M:%S')}] webhook not found!")
                if urlFound:
                    newURL = sendCreate(createURL, "webhook is no longer accessible.", token, config)
                    if newURL:
                        monitorURL = newURL
                        print(f"updated monitor url to: {monitorURL}")
                urlFound = False

            time.sleep(checkInterval)

    except Exception as e:
        print(f"autohook stopped due to an error: {e}")


main()
