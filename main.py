from schedules import get_schedule_message
from bot import bot
from datetime import date


@bot.message_handler(commands=['schedule'])
def schedule_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Loading...')
    schedule_message = get_schedule_message(date.today())
    bot.send_message(chat_id, schedule_message)


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
