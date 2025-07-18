import os
import time
import requests
from telegram import Bot
from datetime import datetime

# Твоят бот токен и чат ID
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("USER_CHAT_ID")

bot = Bot(token=BOT_TOKEN)

# Тук дефинираме примерен токен и API, можеш да смениш с CoinGecko, CMC и др.
TOKEN_SYMBOL = "ethereum"
API_URL = f"https://api.coingecko.com/api/v3/coins/{TOKEN_SYMBOL}"

def fetch_token_data():
    try:
        response = requests.get(API_URL)
        data = response.json()
        price = data['market_data']['current_price']['usd']
        rsi_example = 68  # тук ще добавим реален RSI по-късно
        return price, rsi_example
    except Exception as e:
        return None, None

def send_alert(price, rsi):
    text = f"📊 *{TOKEN_SYMBOL.upper()} Update*\n"
    text += f"💵 Price: ${price}\n"
    text += f"📈 RSI: {rsi}\n"
    text += f"🕒 Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC"
    bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='Markdown')

# Основен цикъл: проверява на всеки 5 часа (18000 секунди)
while True:
    price, rsi = fetch_token_data()
    if price:
        send_alert(price, rsi)
    time.sleep(18000)  # 5 часа
