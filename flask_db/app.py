from flask import Flask, render_template, url_for, request, redirect, flash, send_from_directory
import psycopg2
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

connection = psycopg2.connect(dbname='dkiorasc2un0k', 
                        user='mfsxgnwduulpgm', 
                        password='1fc44e1ed1847d21d2f56365efde7df54727a4a55b55538ddfaaef49340b27ca', 
                        host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS pricol(
                    id SERIAL PRIMARY KEY,
                    login TEXT,
                    password TEXT,
                    coments TEXT
                    );
                 """)
connection.commit()

def clear(len):
    datalen = cursor.execute('SELECT * FROM pricol')
    print(datalen)
    i = 1
    while i <= len:
            cursor.execute(f"""DELETE from pricol where id = {i}""")
            print('del'+str(i))
            i += 1
    connection.commit()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'


@app.route('/get')
def index():
    cursor.execute('SELECT * FROM pricol')
    records = cursor.fetchall()
    return render_template('base.html', records=records)

@app.route('/clear/<int:len>')
def clear_db(len):
    clear(len)
    return redirect('/get')

@app.route('/', methods=['POST', 'GET'])
def new():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']

        print(password != '')
        if login != '' and password != '':
            cursor.execute("INSERT INTO pricol (login, password) VALUES (%s, %s)", (login, password))
            connection.commit()
            return redirect('/get')
        else:
            flash('Заполните форму')
            return redirect('/')
    else:
        return render_template('index.html')

@app.route('/info/<int:id>', methods=['POST', 'GET'])
def info(id):
    cursor.execute(f"""SELECT * FROM pricol WHERE id = {id}""")
    records = cursor.fetchall()
    print(records)
    if request.method == "POST":
        coment = request.form['coment']
        cursor.execute(f"""SELECT coments FROM pricol WHERE id = {id}""")
        coments = cursor.fetchall()
        coments = f'{coment}\n\n\n{coments[0][0]}'
        sql_update_query = """UPDATE pricol SET coments = %s WHERE id = %s"""
        data = (coments, id)
        cursor.execute(sql_update_query, data)

    cursor.execute(f"""SELECT coments FROM pricol WHERE id = {id}""")
    coments = cursor.fetchall()

    if coments == None:
        return render_template(f'info.html', records=records)
    else:
        return render_template(f'info.html', records=records, coments=coments)

 # Папка новых изображений, UPLOAD_PATH - это путь к изображениям
UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'images')
 
@app.route('/upload/',methods=['GET','POST'])
def settings():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        desc = request.form.get('desc')
        avatar = request.files.get('avatar')
                 # Упакуйте имя файла для безопасности, но есть проблема с отображением китайского имени файла
        filename = secure_filename(avatar.filename)
        avatar.save(os.path.join(UPLOAD_PATH,filename))
        print(desc)
        return "Файл загружен успешно"
 
 # Доступ к загруженным файлам
 # Доступ через браузер: http://127.0.0.1:5000/images/django.jpg/ Вы можете просмотреть файл
@app.route('/images/<filename>/',methods=['GET','POST'])
def get_image(filename):
    return send_from_directory(UPLOAD_PATH,filename)
     
if __name__ == "__main__":
     app.run(debug=True)