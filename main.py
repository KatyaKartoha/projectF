from logic import DB_Manager
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types

bot = TeleBot(TOKEN)
hideBoard = types.ReplyKeyboardRemove() 


cancel_button = "Отмена 🚫"
def cansel(message):
    bot.send_message(message.chat.id, "Чтобы посмотреть команды, используй - /info", reply_markup=hideBoard)
  

connection_button = ""
def connection(message):
    bot.send_message(message.chat.id, "777000999", reply_markup=hideBoard)
  
def no_projects(message):
    bot.send_message(message.chat.id, 'Пока участников нет!\nМожешь стать первым с помошью команды /participate')


def gen_inline_markup(rows):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for row in rows:
        markup.add(InlineKeyboardButton(row, callback_data=row))
    return markup

def gen_markup(rows):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 1
    for row in rows:
        markup.add(KeyboardButton(row))
    markup.add(KeyboardButton(connection_button))
    return markup


attributes_of_projects = {'Имя участника' : ["Введите ваше предпочитаемое имя", "user_name"],
                          "Проблема" : ["Введите название проблемы", "problem"],
                          "Статус" : ["Введите статус проблемы", "status"],
                          "Контакт" : ["Введите контактную информацию", "contact_info"]}


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет!👋 Я бот поддержки
Помогу тебе связаться с другими людьми!) 
""")
    info(message)
    
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
"""
Вот команды которые могут тебе помочь:

""")
    



@bot.message_handler(commands=['participate'])
def addtask_command(message):
    bot.send_message(message.chat.id, "Введите своё имя:")
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    name = message.text
    user_id = message.from_user.id
    data = [user_id, name]
    bot.send_message(message.chat.id, "Введите свою проблему")
    bot.register_next_step_handler(message, problem, data=data)

def problem(message, data):
    data.append(message.text)
    statuses = [x[0] for x in manager.get_statuses()] 
    bot.send_message(message.chat.id, "Введите текущий статус проекта", reply_markup=gen_markup(statuses))
    bot.register_next_step_handler(message, callback_project, data=data, statuses=statuses)

def callback_project(message, data, statuses):
    status = message.text
    if message.text == cancel_button:
        cansel(message)
        return
    if status not in statuses:
        bot.send_message(message.chat.id, "Ты выбрал статус не из списка, попробуй еще раз!)", reply_markup=gen_markup(statuses))
        bot.register_next_step_handler(message, callback_project, data=data, statuses=statuses)
        return
    status_id = manager.get_status_id(status)
    data.append(status_id)
    manager.insert_project(tuple(data))
    bot.send_message(message.chat.id, "Проект сохранен \N{smiling face with sunglasses}")
    info(message)






if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()
#Addition to db
#Integration of AI (not decided)
#Keyboard creation