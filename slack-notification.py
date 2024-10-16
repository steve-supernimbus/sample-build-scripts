import argparse
import json
import requests

COLOR = '#9733EE'
ICON_EMOJI = ":bulb:"
CHANNEL = '#channel_name'
USERNAME = 'Jenkins Build Notification Bot'

def slack_webhook(title, message, webhook):
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        webhook,
        headers=headers,
        data=json.dumps(
            slack_notification_content(title, message)
        ),
    )

    if response.status_code == 200:
        log_step("Slack Notification Sent.")
    else:
        log_step(f"Notification Failed, status code: {response.status_code}")

def slack_notification_content(title, message):
    return {
        "channel": CHANNEL,
        "username": USERNAME,
        "icon_emoji": ICON_EMOJI,
        "attachments":
        [
            {
                "color": COLOR,
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
    return parser.parse_args()

if __name__ == '__main__':
    args = get_script_args()
    slack_webhook(args.title, args.message, args.webhook)
