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
@bot.message_handler(func=lambda message: message.chat.id == ADMIN_ID and message.reply_to_message)
def reply_to_user(message):
    original_message_id = message.reply_to_message.message_id  # ID сообщения, на которое админ отвечает
    
    if original_message_id in user_messages:
        user_id = user_messages[original_message_id]  # Получаем ID пользователя
        bot.send_message(user_id, f"Ответ от администратора:\n{message.text}")
    else:
        bot.send_message(ADMIN_ID, "Ошибка: не найден ID пользователя для ответа.")

bot.polling(none_stop=True)
