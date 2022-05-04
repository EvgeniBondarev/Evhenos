import time
import sqlite3
import telebot
from telebot import types
import configure
import requests
import re

BotToken = configure.config['BotToken']
Admin_URL = configure.config['Admin_URL']
AdminId = int(configure.config['AdminId'])
bot = telebot.TeleBot(BotToken)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()


def db_table(user_id: int, user_name: str, user_surname: str, username: str):

    cursor.execute("""CREATE TABLE IF NOT EXISTS us(
        user_id INTEGER,
        user_name TEXT,
        user_surname TEXT,
        username TEXT);
        """)
    cursor.execute(f"SELECT user_id FROM us WHERE user_id={user_id}") 
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO us (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
        conn.commit()
        return True

    else:
        cursor.execute(f"DELETE FROM us WHERE user_id={user_id}")
        conn.commit()
        db_table(user_id, user_name, user_surname, username)
        return False

def del_table(user_id):
    cursor.execute(f"DELETE FROM us WHERE user_id={user_id};")
    conn.commit()
    return True
 

def inf_table(user_id):
    cursor.execute(f"SELECT * FROM us WHERE user_id={user_id};")
    result = cursor.fetchone()
    return result

def admin_info_table():
    cursor.execute(f"SELECT * FROM us;")
    content= cursor.fetchall()
    rez = str(len(content))
    c = []
    for i in range(len(content)):
            content[i] = list(content[i])
            c += content[i]
            for j in range(len(c)):
                c[j] = str(c[j])
                j += 4  
    c.insert(0, ' ')
    for i  in range(len(c)): 
            if i % 4 == 0 and i != 0:
                c[i] = c[i] + '\n\n'

    c = '       '.join(c)
    c = f'''
        User_ID            User_Name           User_Surname                 Username

                {c} 

                                  кол-во участников: {rez}
        '''       
    print(c + str(rez))
    requests.get(f'{Admin_URL}{c}') 
    return c

@bot.message_handler(commands= ['reg'])
def reg(msg):

    us_id = msg.from_user.id
    us_name = msg.from_user.first_name
    us_sname = msg.from_user.last_name
    username = msg.from_user.username

    if db_table(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username) == True:
        bot.send_message(msg.chat.id,  f'<strong>Здраствуйте {msg.from_user.first_name}, регистрация прошла успешено!</strong>\n/inf - Информация о вашей учетной записи\n/del -  Удаление учетной записи', parse_mode='HTML')
        
    else:
        bot.send_message(msg.chat.id,  f'<strong>Учетная запись была изменена</strong>', parse_mode='HTML')
    time.sleep(2)
    bot.delete_message(msg.chat.id, msg.message_id)
    time.sleep(0.5)
    bot.delete_message(msg.chat.id, msg.message_id+1)

@bot.message_handler(commands= ['del'])
def delete(msg):
    if del_table(msg.from_user.id) == True:
        bot.send_message(msg.chat.id,  f'<strong>Учетная запись была удалена</strong>', parse_mode='HTML')
    else:
        bot.send_message(msg.chat.id,  f'<strong>Что-то пошло не так</strong>', parse_mode='HTML')
    time.sleep(2)
    bot.delete_message(msg.chat.id, msg.message_id)
    time.sleep(0.5)
    bot.delete_message(msg.chat.id, msg.message_id+1)

@bot.message_handler(commands= ['inf'])
def info(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    info = inf_table(msg.from_user.id)
    if isinstance(info, tuple) == True:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Закрыть', callback_data='close'))
        bot.send_message(msg.chat.id, text=f"<strong>Имя: {info[1]}\nФамилия: {info[2]}\n<a href='https://t.me/{info[3]}'>Чат с Вами</a>:</strong>", reply_markup=markup, parse_mode='HTML')
    else:
        bot.send_message(msg.chat.id, text=f"<strong>У Вас еще нет учетной зиписи\nдля регистрации введите /reg</strong>", parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def longname(call):
    if call.data == 'close':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 2)

@bot.message_handler(commands= ['admin'])
def admin(msg):
    print(msg.chat.id)
    if msg.chat.id == AdminId:
        admin_info_table()
        bot.send_message(msg.chat.id, text=f"<strong>Отправил в админку</strong>", parse_mode='HTML') 
        time.sleep(2)
        bot.delete_message(msg.chat.id, msg.message_id)
        time.sleep(0.5)
        bot.delete_message(msg.chat.id, msg.message_id + 1)
    else:
        bot.send_message(msg.chat.id, text=f"<strong>Ты не мой отец</strong>", parse_mode='HTML') 
        time.sleep(2)
        bot.delete_message(msg.chat.id, msg.message_id)
        time.sleep(0.5)
        bot.delete_message(msg.chat.id, msg.message_id + 1)


@bot.message_handler(commands= ['start'])
def satrt(msg):
     bot.send_message(msg.chat.id, text=f"<strong>Для дальнейшего использования бота пройдите регистрацию /reg</strong>", parse_mode='HTML')


##############################################################КЛИЕНT################################################################################
PRICE = types.LabeledPrice(label='Настоящая Машина Времени', amount=4200000)

bot.polling(non_stop= True, interval= 0)
