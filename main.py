from schedules import get_schedule_message
from bot import bot
from datetime import datetime
import pytz
from users import add_user
from env import SUPPORT_MESSAGE


def get_today_date():
    now = datetime.now(pytz.timezone('Europe/Kyiv'))
    return now.date()


def save_analytics(message):
    user_id = message.from_user.username or message.chat.id
    add_user(user_id)


def send_support_message(today, chat_id):
    weekday = today.strftime('%A')
    if weekday in ['Friday', 'Saturday', 'Sunday']:
        bot.send_message(chat_id, SUPPORT_MESSAGE, parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(commands=['schedule'])
def schedule_handler(message):
    chat_id = message.chat.id
    loading_message = bot.send_message(chat_id, 'Loading...')
    try:
        today = get_today_date()
        schedule_message = get_schedule_message(today)
        formatted_message = f'<pre>{schedule_message}</pre>'
        bot.delete_message(chat_id, loading_message.message_id)
        bot.send_message(chat_id, formatted_message, parse_mode='HTML')
        save_analytics(message)
        send_support_message(today, chat_id)
    except:
        bot.send_message(chat_id, "Oops, something went wrong")


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
