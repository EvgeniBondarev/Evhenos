from email import message
import re
import time
import sqlite3
import telebot
from telebot import types
import configure        
import requests
import pandas 

BotToken = configure.config['BotToken']
Admin_URL = configure.config['Admin_URL']
AdminId = int(configure.config['AdminId'])
bot = telebot.TeleBot(BotToken)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()


def db_table(user_id: int, user_name: str, user_surname: str, username: str):
    with open("ban_list.txt", encoding='latin-1') as file:
        if str(user_id) in file.read():
            return 'user banned'

        else:
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
            

def del_table(user_id):
    cursor.execute(f"DELETE FROM us WHERE user_id={user_id};")
    conn.commit()
    return True
 

def inf_table(user_id):
    cursor.execute(f"SELECT * FROM us WHERE user_id={user_id};")
    result = cursor.fetchone()
    return result

def admin_info_table():
    id = []
    name = []
    surname = []
    username = []
    cursor.execute(f"SELECT * FROM us;")
    content= cursor.fetchall()
    print(content)
    rez = str(len(content))
    c = []
    for i in range(len(content)):
            content[i] = list(content[i])
            c += content[i]
            for j in range(len(c)):
                c[j] = str(c[j])
                j += 4 
    for j in range(len(c)):
        id.append(c[j])
        if j % 1 and i != 0:
            name.append(c[j])
        if j % 2 and i != 0:
            surname.append(c[j])
        if j % 3 and i != 0:
            username.append(c[j])
        else:
            id.append(c[j])    


    print(f"{id} - id \n {name} - name \n {surname} - surname \n {username} - username")
    '''
    c.insert(0, ' ')
    for i  in range(len(c)): 
            if i % 4 == 0 and i != 0:
                c[i] = c[i] + '\n\n'
    
    
   
    data = {'id': id, 'name': name, 'surname': surname, 'username': username}
    df = pandas.DataFrame.from_dict(data)
    '''

    c = '       '.join(c)
    c = f'''
        User_ID            User_Name           User_Surname                 Username

                {c} 

                                  кол-во участников: {rez}
        '''       
    print(c + str(rez))
    requests.get(f'{Admin_URL}{c}') 
    return c

def ban_user(user_name):
    try:
        cursor.execute("SELECT * FROM us WHERE user_name=?", (user_name,))
        ban_user = cursor.fetchone()
        cursor.execute(f"DELETE FROM us WHERE user_id={ban_user[0]};")

        with open("ban_list.txt", "a") as ban_list:
            ban_list.write(f"{ban_user[0]}\t{ban_user[1]}\n")

        conn.commit()
        return True
    except:
        return False


@bot.message_handler(commands= ['reg'])
def reg(msg):

    us_id = msg.from_user.id
    us_name = msg.from_user.first_name
    us_sname = msg.from_user.last_name
    username = msg.from_user.username

    if db_table(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username) == True:
        bot.send_message(msg.chat.id,  f'<strong>Здраствуйте {msg.from_user.first_name}, регистрация прошла успешено!</strong>\n/inf - Информация о вашей учетной записи\n/del -  Удаление учетной записи', parse_mode='HTML')
    elif db_table(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username) == 'user banned':
        bot.send_message(msg.chat.id,  f'<strong>Вы находитесь в бане. Регистрация невозможна</strong>', parse_mode='HTML')  
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
        #photos = bot.get_user_profile_photos(msg.chat.id)
        #bot.send_message(msg.chat.id, photos.photos[0][0].file_id)
        bot.send_message(msg.chat.id, text=f"<strong>Имя: {info[1]}\nФамилия: {info[2]}\n<a href='https://t.me/{info[3]}'>Чат с Вами</a>:</strong>", reply_markup=markup, parse_mode='HTML')
    else:
        bot.send_message(msg.chat.id, text=f"<strong>У Вас еще нет учетной зиписи,\nдля регистрации введите /reg</strong>", parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def longname(call):
    if call.data == 'close':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 2)

@bot.message_handler(commands= ['info_user'])
def admin(msg):
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

@bot.message_handler(commands= ['ban_user'])
def ban(msg):
    if msg.chat.id == AdminId:
        ban_user_name = ' '.join(msg.text.split(' ')[1:])
        print(type(ban_user_name))
        if (ban_user(ban_user_name) == True):
            bot.send_message(msg.chat.id, text=f"<strong>Пользователь {ban_user_name} удален</strong>", parse_mode='HTML') 
        else:
            bot.send_message(msg.chat.id, text=f"<strong>Пользователя с таким именем нет в базе</strong>", parse_mode='HTML') 
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
     
bot.polling(non_stop= True, interval= 0)