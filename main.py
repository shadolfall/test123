import telebot
import time
from datetime import datetime
import random

BOT_TOKEN = "8415249398:AAEAaPnks-xsB3vfUtX0r79zHhzHzYE6PWc"
ADMIN_ID = 5206203654
CHANNEL_ID = "-1002915789259"

bot = telebot.TeleBot(BOT_TOKEN)

def generate_message_id():
    """Генерирует случайный 6-значный ID"""
    return random.randint(100000, 999999)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, всё что ты сюда напишешь отправится в канал подслушано анонимно! По этому пиши что хочешь. https://t.me/podslyshanoyrtk\n\nPS: Админ не имеет отношение ко всему что происходит в канале и не будет раскрывать личность всех кто отпровил сюда сообщниея")

@bot.message_handler(func=lambda message: True)
def forward_all_messages(message):
    if message.text and message.text.startswith('/'):
        return

    try:
        # Генерируем случайный ID для сообщения
        message_id = generate_message_id()

        # Получаем текст сообщения
        message_text = ""
        if message.text:
            message_text = message.text
        elif message.caption:
            message_text = message.caption
        else:
            message_text = "[Сообщение без текста]"

        formatted_message = f"#{message_id}\n\n{message_text}"

        # Формируем информацию для админа
        username = f"@{message.from_user.username}" if message.from_user.username else "Не указан"
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        admin_info = (
            f"📨 Новое сообщение в канал:\n"
            f"🆔 ID сообщения: #{message_id}\n"
            f"👤 ID пользователя: {message.from_user.id}\n"
            f"📛 Username: {username}\n"
            f"🕒 Время: {current_time}\n"
            f"📝 Текст: {message_text[:100]}{'...' if len(message_text) > 100 else ''}"
        )

        # Отправляем информацию админу
        bot.send_message(ADMIN_ID, admin_info)

        # Отправляем сообщение в канал
        channel_message = None
        if message.text:
            channel_message = bot.send_message(CHANNEL_ID, formatted_message)
        elif message.photo:
            channel_message = bot.send_photo(CHANNEL_ID, message.photo[-1].file_id, caption=formatted_message)
        elif message.video:
            channel_message = bot.send_video(CHANNEL_ID, message.video.file_id, caption=formatted_message)
        elif message.document:
            channel_message = bot.send_document(CHANNEL_ID, message.document.file_id, caption=formatted_message)
        elif message.audio:
            channel_message = bot.send_audio(CHANNEL_ID, message.audio.file_id, caption=formatted_message)
        elif message.voice:
            channel_message = bot.send_voice(CHANNEL_ID, message.voice.file_id, caption=formatted_message)
        else:
            channel_message = bot.forward_message(CHANNEL_ID, message.chat.id, message.message_id)
            bot.send_message(CHANNEL_ID, formatted_message)

        # Отправляем уведомление пользователю
        if channel_message:
            bot.reply_to(message, f"✅ Ваше сообщение #{message_id} было отправлено в канал!")
        else:
            bot.reply_to(message, "❌ Произошла ошибка при отправке сообщения в канал.")

        # Отправляем копию медиа-сообщения админу (если есть медиа)
        if channel_message and not message.text:
            try:
                admin_media_caption = f"Копия сообщения #{message_id}"
                if message.photo:
                    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=admin_media_caption)
                elif message.video:
                    bot.send_video(ADMIN_ID, message.video.file_id, caption=admin_media_caption)
                elif message.document:
                    bot.send_document(ADMIN_ID, message.document.file_id, caption=admin_media_caption)
                elif message.audio:
                    bot.send_audio(ADMIN_ID, message.audio.file_id, caption=admin_media_caption)
                elif message.voice:
                    bot.send_voice(ADMIN_ID, message.voice.file_id, caption=admin_media_caption)
            except Exception as media_error:
                bot.send_message(ADMIN_ID, f"❌ Не удалось отправить медиа админу: {media_error}")

    except Exception as e:
        try:
            bot.reply_to(message, "❌ Произошла ошибка при отправке сообщения в канал.")
            # Уведомляем админа об ошибке
            bot.send_message(ADMIN_ID, f"❌ Ошибка при отправке сообщения в канал: {e}")
        except:
            pass

@bot.message_handler(commands=['test_channel'])
def test_channel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")
        return

    try:
        test_id = generate_message_id()
        test_message = f"#{test_id}\n\nТестовое сообщение от бота. Канал работает корректно!"
        sent_message = bot.send_message(CHANNEL_ID, test_message)

        # Информация админу о тестовом сообщении
        admin_info = (
            f"🧪 Тестовое сообщение:\n"
            f"🆔 ID: #{test_id}\n"
            f"👤 От: {message.from_user.id}\n"
            f"📛 Username: @{message.from_user.username if message.from_user.username else 'Не указан'}\n"
            f"✅ Статус: Успешно отправлено\n"
            f"📊 ID в канале: {sent_message.message_id}"
        )
        bot.send_message(ADMIN_ID, admin_info)

        bot.reply_to(message, f"Тестовое сообщение #{test_id} отправлено в канал! ID: {sent_message.message_id}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при отправке тестового сообщения: {e}")

@bot.message_handler(commands=['stats'])
def show_stats(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")
        return

    try:
        stats_text = (
            "📊 Статистика бота:\n"
            "✅ Бот работает корректно\n"
            "📨 Система использует случайные 6-значные ID\n"
            "🔒 Пользователи остаются анонимными в канале"
        )
        bot.reply_to(message, stats_text)

    except Exception as e:
        bot.reply_to(message, f"Ошибка при получении статистики: {e}")

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except Exception as e:
            time.sleep(10)
