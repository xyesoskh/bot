import telebot
import threading
import time

TOKEN = "8148889670:AAGeNNbk-KHhufgRQ1CYLNeMfQDJf6n8pyE"
ADMIN_ID = 5626257612  # Твой Telegram ID

bot = telebot.TeleBot(TOKEN)
user_messages = {}  # Хранит соответствие message_id ↔ user_id
user_cache = set()  # Храним ID пользователей, чтобы отправить важное сообщение только 1 раз

# Функция для предотвращения сна Railway
def prevent_sleep():
    while True:
        print("👀 Бот не спит!")
        time.sleep(300)  # Пауза в 5 минут

# Запускаем поток, который не даст Railway уснуть
threading.Thread(target=prevent_sleep, daemon=True).start()

# Обработчик сообщений от пользователей
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id

    # Если пользователь пишет впервые и это НЕ администратор, отправляем важное сообщение
    if user_id != ADMIN_ID and user_id not in user_cache:
        bot.send_message(user_id, "⚠️ *ВАЖНОЕ СООБЩЕНИЕ:*\n"
                                  "— Свободный Администратор ответит в ближайшее время.\n"
                                  "— Не отправляйте одно и то же сообщение несколько раз.\n"
                                  "— Если ваш вопрос срочный, уточните это в тексте.", parse_mode="Markdown")
        user_cache.add(user_id)  # Добавляем в кэш, чтобы больше не отправлять

    # Отправляем сообщение админу
    bot.send_message(ADMIN_ID, f"📩 *Сообщение от @{message.chat.username or 'пользователя'}* (ID: {user_id}):\n\n{message.text}", parse_mode="Markdown")

    # Запоминаем, какое сообщение к какому пользователю относится
    user_messages[message.message_id] = user_id

# Обработчик ответов от админа
@bot.message_handler(func=lambda message: message.reply_to_message and message.chat.id == ADMIN_ID)
def reply_to_user(message):
    try:
        original_message_id = message.reply_to_message.message_id  # Получаем ID исходного сообщения
        user_id = user_messages.get(original_message_id)  # Ищем ID пользователя в словаре

        if user_id:
            bot.send_message(user_id, f"📩 *Ответ от администратора:*\n\n{message.text}", parse_mode="Markdown")
            bot.send_message(ADMIN_ID, f"✅ Ответ отправлен пользователю {user_id}!")
        else:
            bot.send_message(ADMIN_ID, "⚠️ Ошибка: Не удалось определить пользователя для ответа.")

    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Ошибка при отправке ответа: {e}")

bot.polling(none_stop=True)
