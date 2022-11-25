from prettytable import PrettyTable
from window import create_table
from datetime import datetime
from create_graph import show_graph

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd 


def data_pars(file_name: str) -> list:

    with open(file_name, 'r', encoding='utf-8') as file:
        records = file.read().split('\n')

    data = []  # [дата], [причина], [смена1], [смена2], [cмена3].
    for i in range(len(records[:-1])):
        data.append(records[i].split('\t'))

    return data


def write_table(file_name: str, table: list):
    with open(file_name, 'w') as file:
        x = PrettyTable()
        x.field_names = ["дата", "Общее время простоя ", "Доля простоя в смене 1 %",
                         "Доля простоя в смене 2 %", "Доля простоя в смене 3 %"]
        for i in table:
            x.add_row(i)

        file.write(str(x))

def date_to_int(string_date: str) -> int:
    arr_date = string_date.split('.')
    int_date = int(arr_date[0]) + (int(arr_date[1]) * 31) + (int(arr_date[2]) * 365)
    return int_date




def data_to_table(data: list) -> list:

    result_data = []  # [дата], [Общее время простоя], [Доля простоя в смене 1 %], [Доля простоя в смене 2 %], [Доля простоя в смене 3 %].
    all_percent = []  # приценты по каждой дате
    for i in range(len(data)):
        date = data[i][0]
        all_time = int(data[i][2]) + int(data[i][3]) + int(data[i][4])
        percent = []
        for j in range(2, len(data[i])):
            percent.append(round((int(data[i][j]) / int(all_time) * 100), 2))

        result_data.append(
            [date, all_time, percent[0], percent[1], percent[2]])
        all_percent.append(percent)

    date_to_graph = [] # список с датами
    [date_to_graph.append(result_data[i][0]) for i in range(len(result_data))]

    result_data.sort(key = lambda x: date_to_int(x[0])) # сортировка по дате
    
    create_table(result_data)
    show_graph(all_percent, date_to_graph)

    return result_data


#table = data_to_table(data_pars('data.txt'))
#write_table('result.txt', table)

def callback():
    name= fd.askopenfilename() 
    print(name)
    but.pack_forget()
    label.pack_forget()
    table = data_to_table(data_pars(name))
    write_table('result.txt', table)


errmsg = 'Error!'
but = tk.Button(text='Выбор файла', 
       command=callback)

label = ttk.Label(text='В текстовом файле находится сводная ведомость о простоях конвейера с начала месяца по некоторому цеху, содержащая пять граф:\n Дата, Причина простоя, Смена 1, Смена 2, Смена3. \nВ последних трех графах указано время простоя в часах.\n\n' + 
                        'Разработайте алгоритм и программу определения времени простоя в каждый день месяца по всем причинам за все смены и долю простоя по каждой смене.' + 
                        'Результаты расчета запишите в новый текстовый файл, содержащий таблицу из пяти граф:\n Дата; Общее время простоя, ч.; Доля простоя в смене 1, %; Доля простоя в смене 2, %; Доля простоя в смене 3, %.\n\n' +
                        'Программа должна обеспечить построение диаграммы долей простоя в сменах '
                  )
label.pack()

but.pack(fill=tk.X)
tk.mainloop()
