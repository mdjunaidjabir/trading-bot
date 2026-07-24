from flask import Flask
from threading import Thread
import telebot
import time
import datetime

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

# 📅 সারাদিনের সিগন্যালের পূর্ণাঙ্গ চার্ট বা তালিকা
signals_chart = [
    "M1  USDPKR-OTC  10:22  PUT  ✅",
    "M1  USDCOP-OTC  10:30  PUT  ✅",
    "M1  USDPKR-OTC  10:31  CALL ✅",
    "M1  USDINR-OTC  10:37  PUT  ✅",
    "M1  CADCHF-OTC  10:45  PUT  ✅",
    "M1  USDPKR-OTC  10:54  PUT  ✅",
    "M1  USDBDT-OTC  11:10  PUT  ✅",
    "M1  USDPKR-OTC  11:27  CALL ✅",
    "M1  USDPKR-OTC  11:30  CALL ✅",
    "M1  USDCOP-OTC  11:34  CALL ✅",
    "M1  USDDZD-OTC  11:36  CALL ✅",
    "M1  USDBDT-OTC  11:44  CALL ✅",
    "M1  CADCHF-OTC  11:57  CALL ✅"
]

print("🤖 সারাদিনের চার্ট পাঠানোর বোট চালু হয়েছে...")

def start_bot():
    sent_today = False

    while True:
        # বাংলাদেশ সময় (UTC+6) ঠিক রাখার হিসাব
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=6)
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%Y-%m-%d")

        # প্রতিদিন সকাল ১০:০০ টায় পুরো চার্ট একসাথে পাঠাবে (সময় চাইলে পরিবর্তন করতে পারেন)
        if current_time == "10:00" and not sent_today:
            chart_text = "\n".join(signals_chart)
            msg = f"🏆 **YT PREMIUM - THE AI FUTURE SIGNALS** 🏆\n\n{chart_text}\n\n🔥 **100% Accuracy AI Bot** 🔥"

            try:
                bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                print("✅ সারাদিনের সিগন্যাল চার্ট পাঠানো হয়েছে!")
                sent_today = True
            except Exception as e:
                print("❌ সমস্যা হয়েছে:", e)

        # রাত ১২টার পর আবার নতুন দিনের জন্য রিসেট হবে
        if current_time == "00:01":
            sent_today = False

        time.sleep(30)

start_bot()
