import time
import random
import threading
from flask import Flask
import telebot

# --- ফ্লাস্ক সার্ভার (বট ২৪ ঘণ্টা সচল রাখার জন্য) ---
app = Flask('')

@app.route('/')
def home():
    return "Batch Trading Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- টেলিগ্রাম বট কনফিগারেশন ---
TOKEN = "আপনার_বট_টোকেন_এখানে_দিন"   # এখানে আপনার টেলিগ্রাম বটের টোকেনটি বসাবেন
CHAT_ID = "@my_trading_signal_2026"  # আপনার টেলিগ্রাম চ্যানেলের ইউজারনেম

bot = telebot.TeleBot(TOKEN)

# ওটিসি কারেন্সি পেয়ারের তালিকা
pairs_pool = ["USDBDT_otc", "USDPKR-OTC", "USDINR-OTC", "EURUSD-OTC", "GBPUSD-OTC"]

def send_batch_signals():
    """একসাথে ১০-২০টি সিগন্যাল একটি মেসেজে পাঠানোর লজিক"""
    while True:
        try:
            # কতগুলো সিগন্যাল একসাথে পাঠাতে চান (যেমন: ১০টি)
            total_signals = 10
            
            signal_list = f"📊 **একসাথে {total_signals}টি ওটিসি সিগন্যাল** 📊\n\n"
            
            for i in range(1, total_signals + 1):
                pair = random.choice(pairs_pool)
                action = random.choice(["CALL 📈", "PUT 📉"])
                signal_list += f"{i}. {pair} — {action} ✅\n"
            
            # টেলিগ্রামে একসাথে পুরো লিস্ট পাঠানো
            bot.send_message(CHAT_ID, signal_list, parse_mode="Markdown")
            
        except Exception as e:
            print(f"ত্রুটি দেখা দিয়েছে: {e}")
            
        # প্রতি ৪০ থেকে ৪৫ মিনিট পর পর পুরো এক ব্যাচ সিগন্যাল পাঠানোর বিরতি
        sleep_time = random.randint(2400, 2700)
        time.sleep(sleep_time)

if __name__ == "__main__":
    keep_alive()
    send_batch_signals()
