from schedules import get_schedule_message
from bot import bot
from datetime import datetime
import pytz
from users import add_user


def get_today_date():
    now = datetime.now(pytz.timezone('Europe/Kyiv'))
    return now.date()


def save_analytics(message):
    user_id = message.from_user.username or message.chat.id
    add_user(user_id)


@bot.message_handler(commands=['schedule'])
def schedule_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Loading...')
    try:
        today = get_today_date()
        schedule_message = get_schedule_message(today)
        formatted_message = f'<pre>{schedule_message}</pre>'
        bot.send_message(chat_id, formatted_message, parse_mode='HTML')
        save_analytics(message)
    except:
        bot.send_message(chat_id, "Oops, something went wrong")


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
