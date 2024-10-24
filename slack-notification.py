import argparse
import json
import requests

def slack_webhook(title, message, urls, webhook, color, icon_emoji, channel, username):
    if urls is None:
        send_slack_message(title, message, webhook, color, icon_emoji, channel, username)
    else:
        urls = process_urls(urls)
        for url in urls:
            send_slack_message(title, url, webhook, color, icon_emoji, channel, username)

def send_slack_message(title, message, webhook, color, icon_emoji, channel, username):
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        webhook,
        headers=headers,
        data=json.dumps(
            slack_notification_content(
                title, message, color, icon_emoji, channel, username
            )
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

def process_urls(urls):
    urls_return = []
    for url in urls.split('\n'):
        url = url.strip()
        url_split = url.split('?')
        urls_return.append(f"<{url}|{url_split[0]}>")
    return urls_return

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
    parser.add_argument("--channel")
    parser.add_argument("--urls", default=None)
    parser.add_argument("--color", default="#9733EE")
    parser.add_argument("--icon-emoji", default=":bulb:")
    parser.add_argument("--username", default="Jenkins Build Notification Bot")
    return parser.parse_args()

if __name__ == '__main__':
    args = get_script_args()
    slack_webhook(
        args.title,
        args.message,
        args.urls,
        args.webhook,
        args.color,
        args.icon_emoji,
        args.channel,
        args.username
    )
