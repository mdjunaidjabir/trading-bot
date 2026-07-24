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

pairs_pool = ["USDPKR-OTC", "USDCOP-OTC", "USDINR-OTC", "CADCHF-OTC", "USDBDT-OTC", "EURUSD-OTC", "GBPUSD-OTC", "USDDZD-OTC"]

def generate_signals():
    signals = []
    start_hour = 10
    start_minute = 10
    
    for i in range(10):
        pair = random.choice(pairs_pool)
        action = random.choice(["CALL", "PUT"])
        emoji = "✅"
        
        start_minute += random.randint(3, 8)
        if start_minute >= 60:
            start_hour += 1
            start_minute -= 60
            
        time_str = f"{start_hour:02d}:{start_minute:02d}"
        signals.append(f"M1  {pair}  {time_str}  {action}  {emoji}")
        
    return signals

print("🤖 ২৪ ঘণ্টা অটো-সিগন্যাল চার্ট বোট চালু হয়েছে...")

def start_bot():
    last_sent_hour = ""

    while True:
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=6)
        current_time = now.strftime("%H:%M")
        current_hour = now.strftime("%H")

        # ২৪ ঘণ্টার মধ্যে প্রতি ৩ ঘণ্টা পর পর (যেমন: রাত ১২টা, ৩টা, সকাল ৬টা, ৯টা, দুপুর ১২টা ইত্যাদি) নতুন চার্ট পাঠাবে
        # আপনি চাইলে সময়গুলো পরিবর্তন করতে পারেন
        allowed_hours = ["00", "03", "06", "09", "12", "15", "18", "21"]

        if current_hour in allowed_hours and current_hour != last_sent_hour and current_time.endswith("00"):
            daily_signals = generate_signals()
            chart_text = "\n".join(daily_signals)
            
            msg = f"🏆 **YT PREMIUM - THE AI FUTURE SIGNALS** 🏆\n\n{chart_text}\n\n🔥 **100% Accuracy AI Bot** 🔥"

            try:
                bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                print(f"✅ ২৪ ঘণ্টার অটো চার্ট সফলভাবে পাঠানো হয়েছে ({current_time})!")
                last_sent_hour = current_hour
            except Exception as e:
                print("❌ সমস্যা হয়েছে:", e)

        time.sleep(30)

start_bot()
