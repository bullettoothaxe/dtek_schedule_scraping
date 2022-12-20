import telebot
from env import BOT_TOKEN
from schedules import get_schedule_message
from datetime import date

bot = telebot.TeleBot(BOT_TOKEN)


# class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
#     key = 'is_chat_admin'
#
#     @staticmethod
#     def check(message: telebot.types.Message):
#         return bot.get_chat_member(message.chat.id, message.from_user.id).status in ['administrator', 'creator']
#
#
# bot.add_custom_filter(IsAdmin())
#
#
# @bot.message_handler(is_chat_admin=True)
# def admin_of_group(message):
#     bot.send_message(message.chat.id, 'You are admin of this group!')

@bot.message_handler(commands=['schedule'])
def start_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Loading...')
    message = get_schedule_message(date.today())
    bot.send_message(chat_id, message)


bot.infinity_polling()
