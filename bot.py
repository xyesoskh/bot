import telebot
import threading
import time

TOKEN = "8148889670:AAGeNNbk-KHhufgRQ1CYLNeMfQDJf6n8pyE"
ADMIN_ID = 5626257612  # Твой Telegram ID


bot = telebot.TeleBot(TOKEN)
user_messages = {}  # Хранит соответствие message_id ↔ user_id

# Функция для предотвращения сна Railway
def prevent_sleep():
    while True:
        print("👀Бот не спит!")
        time.sleep(300)  # Пауза в 5 минут

# Запускаем поток, который не даст Railway уснуть
threading.Thread(target=prevent_sleep, daemon=True).start()

# Получаем сообщения от пользователей и отправляем админу
user_cache = set()  # Храним ID пользователей, чтобы отправить важное сообщение только 1 раз

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id

    # Отправляем админу сообщение от пользователя
    bot.send_message(ADMIN_ID, f"📩 Сообщение от @{message.chat.username or 'без никнейма'} (ID: {user_id}):\n{message.text}")

    # Если пользователь пишет впервые, отправляем важное сообщение
    if user_id not in user_cache:
        bot.send_message(user_id, "⚠️ *ВАЖНОЕ СООБЩЕНИЕ:*\n"
                                  "— Свободный Администратор ответит в ближайшее время.\n"
                                  "— Не отправляйте одно и то же сообщение несколько раз.\n"
                                  "— Если ваш вопрос срочный, уточните это в тексте.", parse_mode="Markdown")
        user_cache.add(user_id)

    # Отправляем стандартное сообщение
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "✅ Ваше сообщение получено! Ожидайте ответа от администратора.")
    user_messages[msg.message_id] = message.chat.id  # Запоминаем, кому ответить

# Обрабатываем ответы админа
ADMIN_ID = 5626257612  # Твой Telegram ID

@bot.message_handler(func=lambda message: message.reply_to_message and str(message.reply_to_message.chat.id) == str(ADMIN_ID))
def reply_to_user(message):
    try:
        # Получаем ID пользователя из пересланного сообщения
        original_message = message.reply_to_message.text
        user_id = original_message.split("(ID: ")[-1].split(")")[0]

        # Отправляем ответ пользователю
        bot.send_message(user_id, f"Ответ от проекта:\n\n{message.text}")

        # Уведомляем админа, что ответ отправлен
        bot.send_message(ADMIN_ID, f"✅ Ответ отправлен!\n🆔 ID: {user_id}\n✉️ Текст: {message.text}")

    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Ошибка при отправке ответа: {e}")
bot.polling(none_stop=True)
