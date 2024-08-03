from logic import DB_Manager
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types
import json
import requests

bot = TeleBot(TOKEN)
hideBoard = types.ReplyKeyboardRemove() 

#headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiODE2MjBmNDktNjQ4My00MTJmLWE4YWItNzdjY2JlYWYzZDA5IiwidHlwZSI6ImFwaV90b2tlbiJ9._0Bd1L9yrN0QYVSg7MNHbBmcSCWxJXqZvOAUGt9zagc"}
url = "https://api.edenai.run/v2/text/chat"
api = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiODE2MjBmNDktNjQ4My00MTJmLWE4YWItNzdjY2JlYWYzZDA5IiwidHlwZSI6ImFwaV90b2tlbiJ9._0Bd1L9yrN0QYVSg7MNHbBmcSCWxJXqZvOAUGt9zagc"
def generate(text):
    headers = {"Authorization": f"Bearer {api}"}
    ur = f"{url}"
    payload = {
    "providers": "openai, cohere",
    "text": f"{text}",
    "temperature" : 0.2,
    "max_tokens" : 250 }
    response = requests.post(ur, json=payload, headers=headers)
    result = json.loads(response.text)
    return result['openai']['generated_text']

cancel_button = "Отмена 🚫"
def cansel(message):
    bot.send_message(message.chat.id, "Чтобы посмотреть команды, используй - /info", reply_markup=main_markup())
  
def main_markup():
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('SOS'))
    return markup

def support_markup():
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton(cancel_button))
    return markup

def gen_inline_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(cancel_button, callback_data='cancel'))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cancel":
        cansel(call.message)

def gen_markup(rows):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 1
    for row in rows:
        markup.add(KeyboardButton(row))
    markup.add(KeyboardButton(cancel_button))
    return markup

  
def no_participants(message):
    bot.send_message(message.chat.id, 'Можешь стать участником с помошью команды /participate')

# def gen_markup(rows):
#     markup = ReplyKeyboardMarkup(one_time_keyboard=False)
#     markup.row_width = 1
#     for row in rows:
#         markup.add(KeyboardButton(row))
#     markup.add(KeyboardButton(button_help))
#     return markup


attributes_of_projects = {'Имя участника' : ["Введите ваше предпочитаемое имя", "user_name"],
                          "Проблема" : ["Введите название проблемы", "problem"],
                          "Статус" : ["Введите статус проблемы", "status_id"],
                          "Контакт" : ["Введите контактную информацию", "contact_info"]}


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет!👋 Я бот поддержки
Помогу тебе связаться с другими людьми!) 
""", reply_markup=main_markup())
    info(message)
    
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
"""
Вот команды которые могут тебе помочь:
/start - Старт программы
/info - То, что вы читаете сейчас :]
/participate - Принять участие в проекте
/description -  Дополнительное описание вашей (проблемы) проблемы
/details -  Добавить дополнительное описание вашей проблемы, что бы помочь другим распознать её
/seek - Поиск участников с похожей проблемой
/found - Поиск определенного участника (осуществляется по имени)
Если Вам необходим контакт для связи со специалистом (Б, К, Р) Введите SOS или нажмите на кнопку
""", reply_markup=main_markup())
    


@bot.message_handler(commands=['participate'])
def addtask_command(message):
    bot.send_message(message.chat.id, "Введите своё имя:", reply_markup=support_markup())
    bot.register_next_step_handler(message, user_name)
 
def user_name(message):
    if message.text == cancel_button:
        cansel(message)
        return
    name = message.text.lower()
    user_id = message.from_user.id
    data = [user_id, name]
    bot.send_message(message.chat.id, "Введите свою проблему", reply_markup=support_markup())
    bot.register_next_step_handler(message, problem, data=data)
    print(data)

def problem(message, data):
    if message.text == cancel_button:
        cansel(message)
        return
    #problemka = message.text
    data.append(message.text.lower())
    #data = [problemka]
    bot.send_message(message.chat.id, "Введите статус проблемы", reply_markup=support_markup())
    bot.register_next_step_handler(message, problem_status, data=data)
    print(data)

def problem_status(message, data):
    if message.text == cancel_button:
        cansel(message)
        return
    #state = message.text
    data.append(message.text.lower())
    #data = [user_id, problemka]
    bot.send_message(message.chat.id, "Введите контакт", reply_markup=support_markup())
    bot.register_next_step_handler(message, contact, data=data)
    print(data)

def contact(message, data):
    if message.text == cancel_button:
        cansel(message)
        return
    #my_con = message.text
    data.append(message.text.lower())
    print(data)
    manager.insert_problem(tuple(data))
    bot.send_message(message.chat.id, "Done")





@bot.message_handler(commands=['details'])
def deet_handler(message):
    bot.send_message(message.chat.id, 'Please enter your problem', reply_markup=support_markup())
    user_id = message.from_user.id
    apply = [user_id]
    #projects = manager.get_participance(user_id)
    bot.register_next_step_handler(message, detailer, apply=apply)

def detailer(message, apply):
    if message.text == cancel_button:
        cansel(message)
        return
    problem_name = message.text
    apply.append(problem_name.lower())
    bot.send_message(message.chat.id, 'Оставь комментарий для других пользователей', reply_markup=support_markup())
    bot.register_next_step_handler(message, set_deets, apply=apply)

def set_deets(message, apply):
    description = message.text
    if message.text == cancel_button:
        cansel(message)
        return
    apply.append(description)
    manager.insert_deets(tuple(apply))
    bot.send_message(message.chat.id, f'Ваше описание к проблеме добавлено ')

@bot.message_handler(commands=['description'])
def desc_search_handler(message):
    bot.send_message(message.chat.id, 'Enter your problem', reply_markup=support_markup())
    # prob = message.text
    bot.register_next_step_handler(message, get_prob)

def get_prob(message):
    prob_for_deets = message.text.lower()
    if message.text == cancel_button:
        cansel(message)
        return
    bot.send_message(message.chat.id, "Вот что нашлось")
    #bot.register_next_step_handler(message, continuation, prob=prob)
    desc_get(message, prob_for_deets)

def desc_get(message, prob_for_deets):
    figured = manager.get_deets(prob_for_deets)
    if figured:
        text = "\n".join([f"\nDescription: {x[2]}" for x in figured])
        bot.send_message(message.chat.id, prob_for_deets + text)
    else:
    #     print(info[0][1], info[0][2], info[0][3], info[0][4] )
        bot.send_message(message.chat.id, 'Похоже ничего подобного не нашлось' )


@bot.message_handler(commands=['seek'])
def participants_handler(message):
    bot.send_message(message.chat.id, 'Enter your problem', reply_markup=support_markup())
    # prob = message.text
    bot.register_next_step_handler(message, prob_con)

def prob_con(message):
    prob = message.text.lower()
    if message.text == cancel_button:
        cansel(message)
        return
    bot.send_message(message.chat.id, "Вот что нашлось")
    #bot.register_next_step_handler(message, continuation, prob=prob)
    continuation(message, prob)

def continuation(message, prob):
    info = manager.get_participants(prob)
    if info:
        text = "\n".join([f"Name: {x[1]} \nProblem: {x[2]} \nStatus: {x[3]} \nContact: {x[4]}\n" for x in info])
        bot.send_message(message.chat.id, text)
    else:
    #     print(info[0][1], info[0][2], info[0][3], info[0][4] )
        bot.send_message(message.chat.id, 'Похоже ничего подобного не нашлось' )


@bot.message_handler(commands=['found'])
def participants_handler(message):
    bot.send_message(message.chat.id, 'Enter the name of participant in search', reply_markup=support_markup())
    # prob = message.text
    bot.register_next_step_handler(message, cont)

def cont(message):
    named = message.text.lower()
    if message.text == cancel_button:
        cansel(message)
        return
    bot.send_message(message.chat.id, "Вот что нашлось(/found)")
    #bot.register_next_step_handler(message, contin, named=named)
    contin(message, named)

def contin(message, named):
    info_cert = manager.get_participant_cert(named)
    if info_cert:
        text = "\n".join([f"Name: {x[1]} \nProblem: {x[2]} \nStatus: {x[3]} \nContact: {x[4]}\n" for x in info_cert])
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Похоже никого подобного не нашлось' )
        no_participants(message)#     print(info[0][1], info[0][2], info[0][3], info[0][4]



@bot.message_handler(func=lambda message: True)
def sos_message(message):
    string = "SOS"
    if message.text == string:
        bot.send_message(message.chat.id, f"Свяжитесь со специалистом по нужному номеру:\n \nМеждународная гуманитарная организация 'Человек в беде' (People in Need, PIN): 0 800 210 160\n \nРоссия(): +7 495 989-50-50 или 8 (800) 333-44-34\n \nКазахстан: +7 708 983 28 63 и +7 727 376 56 60 или 150\n \nБелорусь: 8(801) 100 16 11(для несовершеннолетних)\n \nУкраина: 0 800 331 800 (до 19:00) или 7333(круглосуточно, предотвращение самоубийств)\n \n Кыргызстан: 111(детский) или -")
    else:
        #generate(message.text)
        bot.send_message(message.chat.id, generate(message.text))


if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()
#Addition to db
#Integration of AI (not decided)
#Keyboard creation