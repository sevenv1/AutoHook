# AutoHook

AutoHook is a Python script that monitors a Discord webhook URL and automatically recreates it if it becomes inaccessible (e.g, deleted). This ensures continuous availability of webhooks for integrations (if the webhook is public).

## Features
- Monitors a specified webhook URL at certain intervals.
- Detects if the webhook is deleted or unreachable.
- Creates a new webhook.
- Updates the configuration with the new webhook URL.
- Simple configuration via JSON file.

## Requirements
- Python 3.x
- pip install requests

## Configuration
Edit `config.json` with the following settings:
- `token`: Your Discord account token (for authorization).
- `monitorURL`: The webhook URL to monitor (e.g., a Discord webhook link).
- `createURL`: The endpoint to create a new webhook (e.g., `https://discord.com/api/v9/webhooks/{channel_id}/webhooks`).
- `checkInterval`: Time in seconds between checks (default: 1).

Example `config.json`:
```json
{
  "token": "discord_token",
  "monitorURL": "https://discord.com/api/webhooks/...",
  "createURL": "https://discord.com/api/v9/webhooks/12345678915/webhooks",
  "checkInterval": 1
}
```

## Usage
1. Configure `config.json` as described.
2. Run the script: `python main.py`
3. The script will start monitoring the webhook and log status updates.
4. If the webhook is deleted, it will attempt to create a new one and update the config.

## Notes
- The script runs in an infinite loop.
- Ensure your token has permissions to create webhooks in the specified channel.
- This tool is for personal use; comply with Discord's Terms of Service.
