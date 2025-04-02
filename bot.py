import telebot

TOKEN = "8148889670:AAGeNNbk-KHhufgRQ1CYLNeMfQDJf6n8pyE"
ADMIN_ID = 5626257612  # Твой Telegram ID

bot = telebot.TeleBot(TOKEN)
user_messages = {}  # Хранит соответствие message_id ↔ user_id

# Получаем сообщения от пользователей и отправляем админу
@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID)
def forward_to_admin(message):
    msg = bot.send_message(
        ADMIN_ID, 
        f"Сообщение от @{message.chat.username or 'Без имени'} (ID: {message.chat.id}):\n\n{message.text}"
    )
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
        bot.send_message(user_id, f"Ответ от администратора:\n{message.text}")

        # Уведомляем админа, что ответ отправлен
        bot.send_message(ADMIN_ID, f"✅ Ответ отправлен!\n🆔 ID: {user_id}\n✉️ Текст: {message.text}")

    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Ошибка при отправке ответа: {e}")
bot.polling(none_stop=True)
