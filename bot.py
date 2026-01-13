import os
import telebot
import sqlite3
import time

# التوكن من متغيرات السيرفر (Railway Variables)
TOKEN = os.getenv("8330484091:AAGs2EknopII1LuBYeLFmUwzLfmsuu7ESSQ")

if not TOKEN:
    print("ERROR: TOKEN not found in environment variables")
    exit(1)

bot = telebot.TeleBot(TOKEN, threaded=True)

# ===== Database =====
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    join_date TEXT
)
""")
conn.commit()

def save_user(user):
    cur.execute("SELECT id FROM users WHERE id=?", (user.id,))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO users VALUES (?, ?, ?, datetime('now'))",
            (user.id, user.username, user.first_name)
        )
        conn.commit()

# ===== Commands =====

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user)
    bot.reply_to(message, "👋 مرحبا بك في مجتمع الأمن السيبراني والبرمجة!")

@bot.message_handler(commands=['profile'])
def profile(message):
    user = message.from_user
    cur.execute("SELECT join_date FROM users WHERE id=?", (user.id,))
    row = cur.fetchone()

    text = f"""
👤 الملف الشخصي

ID: {user.id}
الاسم: {user.first_name}
اليوزر: @{user.username}
تاريخ الانضمام: {row[0] if row else 'غير معروف'}
"""
    bot.reply_to(message, text)

# ===== Run =====
while True:
    try:
        print("Bot running...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print("Error, retrying in 5s:", e)
        time.sleep(5)
