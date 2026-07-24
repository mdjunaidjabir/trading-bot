import time
import random
import threading
from flask import Flask
import telebot

app = Flask('')

@app.route('/')
def home():
    return "Batch Trading Bot is running successfully!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# আপনার আসল বট টোকেনটি এখানে বসাবেন
TOKEN = "8805175487:AAHb1immvqQinBYjbViy2D01IIoD3p8HcOY"
CHAT_ID = "@my_trading_signal_2026"

bot = telebot.TeleBot(TOKEN)
pairs_pool = ["USDBDT_otc", "USDPKR-OTC", "USDINR-OTC", "EURUSD-OTC", "GBPUSD-OTC"]

def send_batch_signals():
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
            
        time.sleep(1800)

if __name__ == "__main__":
    keep_alive()
    send_batch_signals
