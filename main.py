import time
import random
import threading
from flask import Flask
import telebot

app = Flask('')

@app.route('/')
def home():
    return "Trading Bot is Live!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# আপনার টেলিগ্রাম বট টোকেন এবং চ্যাট আইডি এখানে দিন
TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "@my_trading_signal_2026"

bot = telebot.TeleBot(TOKEN)
pairs_pool = ["USDBDT_otc", "USDPKR-OTC", "USDINR-OTC", "EURUSD-OTC", "GBPUSD-OTC"]

def send_signals():
    while True:
        try:
            total_signals = 10
            signal_list = f"📊 **একসাথে {total_signals}টি ওটিসি সিগন্যাল** 📊\n\n"
            
            for i in range(1, total_signals + 1):
                pair = random.choice(pairs_pool)
                action = random.choice(["CALL 📈", "PUT 📉"])
                signal_list += f"{i}. {pair} — {action} ✅\n"
            
            bot.send_message(CHAT_ID, signal_list, parse_mode="Markdown")
        except Exception as e:
            print(f"Error: {e}")
            
        time.sleep(1800) # প্রতি ৩০ মিনিট পর পর সিগন্যাল পাঠাবে

if __name__ == "__main__":
    keep_alive()
    send_signals()
