import telebot
import time
import datetime

TOKEN = "8805175487:AAHb1immvqQinBYjbViy2D01IIoD3pHc0Y"
CHAT_ID = "@my_trading_signal_2026"

bot = telebot.TeleBot(TOKEN)

# 📅 আপনার সারাদিনের সিগন্যাল সময় (২৪ ঘণ্টার ফরম্যাটে লিখবেন)
signals_list = [
    {"time": "10:00", "pair": "USDBDT_otc", "action": "CALL"},
    {"time": "14:30", "pair": "CADCHF_otc", "action": "PUT"},
    {"time": "20:00", "pair": "EURUSD_otc", "action": "CALL"},
]

print("🤖 ট্রেডিং সিগন্যাল বোট সার্ভারে চালু হয়েছে...")

def start_bot():
    sent_signals = []

    while True:
        # বাংলাদেশ সময় (UTC+6) ঠিক রাখার হিসাব
        now = (datetime.datetime.utcnow() + datetime.timedelta(hours=6)).strftime("%H:%M")
        
        for item in signals_list:
            if item["time"] == now and item["time"] not in sent_signals:
                msg = f"{item['time']}  {item['pair']}  {item['action']}  ✅"
                
                try:
                    bot.send_message(CHAT_ID, msg)
                    print(f"[{now}] ✅ সিগন্যাল পোস্ট হয়েছে: {msg}")
                    sent_signals.append(item["time"])
                except Exception as e:
                    print("❌ সমস্যা হয়েছে:", e)
        
        time.sleep(5)

start_bot()
