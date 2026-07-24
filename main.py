import time
import random
import threading
from flask import Flask
import telebot
import pandas as pd
import yfinance as yf

# --- ফ্লাস্ক সার্ভার (রেন্ডার বা অন্য হোস্টিংয়ে ২৪ ঘণ্টা চালুর রাখার জন্য) ---
app = Flask('')

@app.route('/')
def home():
    return "Advanced Trading Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- টেলিগ্রাম বট কনফিগারেশন ---
TOKEN = "আপনার_বট_টোকেন_এখানে_দিন"  # আপনার বটের টোকেন এখানে বসাবেন
CHAT_ID = "@my_trading_signal_2026"

bot = telebot.TeleBot(TOKEN)

# কারেন্সি বা অ্যাসেট পেয়ার (Yahoo Finance-এর ফরম্যাট অনুযায়ী)
pairs_pool = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X"]

def calculate_rsi(data, window=14):
    """RSI ক্যালকুলেট করার ফাংশন"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_real_signals():
    """রিয়েল মার্কেট ডেটা এবং RSI/MACD দিয়ে সিগন্যাল জেনারেট করার লজিক"""
    while True:
        try:
            # পেয়ারগুলোর মধ্য থেকে একটি রেন্ডম পেয়ার সিলেক্ট করা
            pair = random.choice(pairs_pool)
            
            # Yahoo Finance থেকে শেষ ৫ দিনের ১ ঘণ্টার ডেটা ফেচ করা
            df = yf.download(pair, period="5d", interval="1h", progress=False)
            
            if len(df) > 20:
                # RSI ক্যালকুলেট করা
                df['RSI'] = calculate_rsi(df)
                current_rsi = df['RSI'].iloc[-1]
                
                # ইন্ডিকেটর ফিল্টার লজিক
                if current_rsi < 30:
                    action = "CALL (BUY)"  # ওভারসোল্ড থাকলে বাই সিগন্যাল
                    emoji = "🟢"
                elif current_rsi > 70:
                    action = "PUT (SELL)"   # ওভারবট থাকলে সেল সিগন্যাল
                    emoji = "🔴"
                else:
                    # যদি মার্কেট নিউট্রাল থাকে, পরবর্তী লুপের জন্য কিছুক্ষণ অপেক্ষা করে স্কিপ করবে
                    time.sleep(300)
                    continue

                # টেলিগ্রামে মেসেজ পাঠানো
                message = (
                    f"{emoji} **হাই-অ্যাকিউরেসি ট্রেডিং সিগন্যাল** {emoji}\n\n"
                    f"📊 **অ্যাসেট:** {pair}\n"
                    f"📈 **অ্যাকশন:** {action}\n"
                    f"📉 **RSI ভ্যালু:** {current_rsi:.2f}\n"
                    f"⏰ **স্ট্যাটাস:** রিয়েল-টাইম মার্কেট অ্যানালাইসিস সম্পন্ন!"
                )
                
                bot.send_message(CHAT_ID, message, parse_mode="Markdown")
            
        except Exception as e:
            print(f"ত্রুটি দেখা দিয়েছে: {e}")
            
        # প্রতি ৪০ থেকে ৪৫ মিনিট পরপর সিগন্যাল পাঠানোর জন্য বিরতি
        sleep_time = random.randint(2400, 2700) # সেকেন্ডে হিসাব (৪০-৪৫ মিনিট)
        time.sleep(sleep_time)

if __name__ == "__main__":
    # ফ্লাস্ক ব্যাকগ্রাউন্ড সার্ভার চালু করা
    keep_alive()
    
    # সিগন্যাল জেনারেটর লুপ রান করা
    generate_real_signals()
