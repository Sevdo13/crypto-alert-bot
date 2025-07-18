import time
import requests
import logging
from telegram import Bot

# === НАСТРОЙКИ ===
TOKEN = "7376425928:AAGD1h8J29xaE30PSIl7RudVJxtzZoLd2mc"  # твоят Telegram бот токен
CHAT_ID = "тук-въведи-своя-chat-id"  # твоя Telegram ID (ще ти кажа как да го намериш)

# Списък с токени, които ще се наблюдават
TOKENS = ["OP", "PENGU", "PYTH"]  # можеш да добавяш още

# Функция за получаване на пазарни данни
def get_token_data(symbol):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": "",
            "symbols": symbol.lower(),
            "order": "market_cap_desc",
            "per_page": 1,
            "page": 1,
            "sparkline": "false"
        }
        response = requests.get(url, params=params)
        data = response.json()
        return data[0] if data else None
    except Exception as e:
        logging.error(f"Грешка при взимане на данни за {symbol}: {e}")
        return None

# Функция за изпращане на Telegram съобщение
def send_telegram_message(message):
    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

# Главен цикъл
def monitor_tokens():
    last_data = {}
    while True:
        for symbol in TOKENS:
            data = get_token_data(symbol)
            if data:
                price = data.get("current_price", 0)
                change = data.get("price_change_percentage_24h", 0)
                if symbol not in last_data or abs(change - last_data[symbol]) > 5:
                    message = f"📈 {symbol.upper()} Update:\nЦена: ${price:.3f}\nПромяна 24ч: {change:.2f}%"
                    send_telegram_message(message)
                    last_data[symbol] = change
        time.sleep(5 * 60 * 60)  # изчакай 5 часа

if __name__ == "__main__":
    monitor_tokens()
