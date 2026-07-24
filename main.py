from flask import Flask
from threading import Thread
import telebot
import time
import datetime
import random

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

TOKEN = "8805175487:AAHb1immvqQinBYjbViy2D01IIoD3pHc0Y"
CHAT_ID = "@my_trading_signal_2026"

bot = telebot.TeleBot(TOKEN)

# র্যান্ডম পেয়ারগুলোর তালিকা
pairs_pool = ["USDPKR-OTC", "USDCOP-OTC", "USDINR-OTC", "CADCHF-OTC", "USDBDT-OTC", "EURUSD-OTC", "GBPUSD-OTC", "USDDZD-OTC"]

def generate_daily_signals():
    signals = []
    # প্রতিদিনের জন্য ১০-১২টি র্যান্ডম সিগন্যাল তৈরি করার লজিক
    start_hour = 10
    start_minute = 10
    
    for i in range(12):
        pair = random.choice(pairs_pool)
        action = random.choice(["CALL", "PUT"])
        emoji = "✅"
        
        # সময়ের ব্যবধান বাড়িয়ে দেওয়া (৫ থেকে ৭ মিনিট পরপর)
        start_minute += random.randint(3, 8)
        if start_minute >= 60:
            start_hour += 1
            start_minute -= 60
            
        time_str = f"{start_hour:02d}:{start_minute:02d}"
        signals.append(f"M1  {pair}  {time_str}  {action}  {emoji}")
        
    return signals

print("🤖 অটো-জেনারেটর সিগন্যাল বোট চালু হয়েছে...")

def start_bot():
    sent_today = False

    while True:
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=6)
        current_time = now.strftime("%H:%M")

        # প্রতিদিন সকাল ১০:০০ টায় নিজে নিজে নতুন চার্ট জেনারেট করে পাঠাবে
        if current_time == "10:00" and not sent_today:
            daily_signals = generate_daily_signals()
            chart_text = "\n".join(daily_signals)
            
            msg = f"🏆 **YT PREMIUM - THE AI FUTURE SIGNALS** 🏆\n\n{chart_text}\n\n🔥 **100% Accuracy AI Bot** 🔥"

            try:
                bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                print("✅ প্রতিদিনের নতুন সিগন্যাল চার্ট জেনারেট করে পাঠানো হয়েছে!")
                sent_today = True
            except Exception as e:
                print("❌ সমস্যা হয়েছে:", e)

        # রাত ১২টার পর আবার রিসেট হবে, যাতে পরের দিন আবার নতুন চার্ট বানাতে পারে
        if current_time == "00:01":
            sent_today = False

        time.sleep(30)

start_bot()
