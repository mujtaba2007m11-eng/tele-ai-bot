from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

Thread(target=run).start()

import telebot
from telebot import types
from g4f.client import Client

# توكن البوت الخاص بك
TELEGRAM_TOKEN = "8736910960:AAGYBsnb1WCd0sFf97t17-Jdkn4CuhTBNpc"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
ai_client = Client()

# لوحة الأزرار
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_ask = types.InlineKeyboardButton("🤖 اسأل الذكاء الاصطناعي", callback_data="ai_help")
    btn_iphone = types.InlineKeyboardButton("📱 شروحات الآيفون", callback_data="iphone_help")
    btn_about = types.InlineKeyboardButton("💡 حول البوت", callback_data="about_bot")
    markup.add(btn_ask, btn_iphone)
    markup.add(btn_about)
    return markup

@bot.message_handler(commands=['start'])
def start_cmd(message):
    name = message.from_user.first_name
    text = f"أهلاً وسهلاً بك يا {name}! 🌟\nاختر من الأزرار أو اكتب أي سؤال وسأجيبك فوراً:"
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "ai_help":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "اكتب أي سؤال وسأجيبك فوراً وبذكاء!")
    elif call.data == "iphone_help":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📱 قسم تقنيات الآيفون والشهادات وتطبيقات IPA.")
    elif call.data == "about_bot":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "💡 المساعد الذكي: بوت آلي مدعوم بالذكاء الاصطناعي بدون قيود.")

# الرد الذكي المباشر (بدون API Key)
@bot.message_handler(func=lambda msg: True)
def chat_with_ai(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = ai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": message.text}]
        )
        answer = response.choices[0].message.content
        bot.reply_to(message, answer)
    except Exception as e:
        bot.reply_to(message, "حدث ضغط على السيرفر، يرجى إعادة إرسال السؤال مرة أخرى.")
        print(f"Error: {e}")

print("تم تفعيل البوت بنجاح! جاهز في تليجرام...")
bot.infinity_polling(timeout=20, long_polling_timeout=10)
