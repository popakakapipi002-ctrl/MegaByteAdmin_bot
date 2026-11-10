import os
import telebot
from flask import Flask, request, jsonify

# --- НАСТРОЙКИ ---
BOT_TOKEN = '9196534345:AAHo_yMuLoLiKgEDdwIvdBeluNN_SLX1Mz4'
ADMIN_IDS = [1277087710]

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Я бот для приема заявок с сайта МЕГАБАЙТ")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    text = (
        f"🔥 <b>НОВАЯ ЗАЯВКА!</b>\n\n"
        f"👤 <b>Имя:</b> {data.get('name')}\n"
        f"📞 <b>Телефон:</b> {data.get('phone')}\n"
        f"🎮 <b>Формат:</b> {data.get('type')}\n"
        f"📅 <b>Дата:</b> {data.get('date')}\n"
        f"⏰ <b>Время:</b> {data.get('time')}"
    )
    
    for admin_id in ADMIN_IDS:
        try:
            bot.send_message(admin_id, text, parse_mode='HTML')
        except Exception as e:
            print(f"Ошибка отправки {admin_id}: {e}")
            
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    import threading
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
