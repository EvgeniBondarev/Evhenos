from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
 
root = Tk()
root.title("Data")
root.geometry("1000x800") 
 
def create_table(data: list):
    img = ImageTk.PhotoImage(Image.open("foo.png"))
    b = Label(image = img)
    b.pack()


    people = data
     
    # определяем столбцы
    columns = ("data", "all_data", "smen1", "smen2", "smen3")
     
    tree = ttk.Treeview(columns=columns, show="headings")
    tree.pack(fill=BOTH, expand=1)
     
    # определяем заголовки
    tree.heading("data", text="Дата")
    tree.heading("all_data", text="Общее время простоя")
    tree.heading("smen1", text="Доля простоя в смене 1 %")
    tree.heading("smen2", text="Доля простоя в смене 2 %")
    tree.heading("smen3", text="Доля простоя в смене 3 %")
     
    # добавляем данные
    for person in people:
        tree.insert("", END, values=person)
     
    root.mainloop()