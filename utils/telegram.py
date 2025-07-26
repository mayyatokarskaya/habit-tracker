import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


def send_telegram_message(text: str):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram token or chat ID not configured.")
        return

    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        response = requests.post(TELEGRAM_API_URL, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Telegram error: {e}")
