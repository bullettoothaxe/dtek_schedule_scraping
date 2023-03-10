import telebot
from env import BOT_TOKEN
import users

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    welcome_message = 'Welcome to the Light Bot! \nYou can open the "Menu" section to explore the bot possibilities.'
    bot.send_message(chat_id, welcome_message)


@bot.message_handler(commands=['users_anal'])
def users_anal_handler(message):
    chat_id = message.chat.id
    active_users = users.read()
    message = f"Users count: {len(active_users)}"
    bot.send_message(chat_id, message)

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
