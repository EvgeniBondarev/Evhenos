from random import randint
import sqlite3
from turtle import back

global db, sql



db = sqlite3.connect('server.db')#создание таблицы
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users( 
	login TEXT,
	password TEXT, 
	cash BIGINT

)""")#создание столбцов

db.commit()

def reg():
	user_login = input('Веди свой логин:')
	user_password = input('Введите пароль:')

	sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'") 

	if sql.fetchone() is None:
		sql.execute(f"INSERT INTO users VALUES (?, ?, ?)", (user_login, user_password, 0))
		db.commit()
		print('Регистрация прошла успашно!')
	else:
		print('Такая запись уже есть')

		for value in sql.execute("SELECT * FROM users"):
			print(value)

def delite_db():
	sql.execute(f"DELETE FROM users WHERE login = '{user_login}'")
	db.commit()
	print('Запись удалена')
	for value in sql.execute("SELECT * FROM users"):
			print(value)

def casino():
	global user_login
	user_login = input('log in:')
	number = randint(1, 2)

	sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'") 

	if sql.fetchone() is None: 
		print('Логин не найден. Пройдите регистрацию')
		reg()
	else:
		if number == 1:
			sql.execute(f"UPDATE users SET cash = cash + 1000 WHERE login = '{user_login}'")
			sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'") 
			rez = sql.fetchone()
			print('Вы выйграли! Ваш баланс: ' + str(rez[0]))
			db.commit()
		else:
			print('Вы проиграли!')
			delite_db()

def enter():
	for i in sql.execute("SELECT login, cash FROM users"):
		print(i)

def main():
	casino()
	enter()
main()


