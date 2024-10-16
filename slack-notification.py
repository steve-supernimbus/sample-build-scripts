import argparse
import json
import requests

def slack_webhook(title, message, webhook, color, icon_emoji, channel, username):
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        webhook,
        headers=headers,
        data=json.dumps(
            slack_notification_content(title, message, color, icon_emoji, channel, username)
        ),
    )

    if response.status_code == 200:
        log_step("Slack Notification Sent.")
    else:
        log_step(f"Notification Failed, status code: {response.status_code}")

def slack_notification_content(title, message, color, icon_emoji, channel, username):
    return {
        "channel": channel,
        "username": username,
        "icon_emoji": icon_emoji,
        "attachments":
        [
            {
                "color": color,
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }

def log_step(step):
    separator = "===================================================="
    print(separator)
    print(f"Step: {step}")
    print(separator)
    print("\n")

def get_script_args():
    parser = argparse.ArgumentParser(description="Slack Notification Script")
    parser.add_argument("--title")
    parser.add_argument("--message")
    parser.add_argument("--webhook")
    parser.add_argument("--color", default="#9733EE")
    parser.add_argument("--icon-emoji", default=":bulb:")
    parser.add_argument("--channel", default="#channel_name")
    parser.add_argument("--username", default="Jenkins Build Notification Bot")
    return parser.parse_args()

if __name__ == '__main__':
    args = get_script_args()
    slack_webhook(
        args.title,
        args.message,
        args.webhook,
        args.color,
        args.icon_emoji,
        args.channel,
        args.username
    )
