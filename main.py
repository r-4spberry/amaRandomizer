# -*- coding: WINDOWS-1251 -*-
from this import d
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from random import choice
from PIL import Image, ImageTk
# create root window
root = Tk()

class popupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Input a new group name")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()


def add():
    global attrs
    global types
    if types.get() == 'Add new':
        ans = ""
        while ans == "":
            input = popupWindow(root.master)
            root.wait_window(input.top)
            ans = input.value
            if ans == "":
                root.bell()
    files = fd.askopenfilenames(filetypes = (("Image", "*.png"), ))
    if len(files) != 0:
        if types.get() in attrs:
            attrs[types.get()] += list(files)
        else:
            types["values"] = types["values"] + (input.value, )
            types.set('Add new')
            attrs[input.value] = list(files)

def delete():
    if types.get() != "Add new":
        del attrs[types.get()]
        arr = list(types["values"])
        print(arr)
        print(arr.index(types.get()))
        arr.pop(arr.index(types.get()))
        types["values"] = tuple(arr)
        types.set(types["values"][-1])

def generate():
    global canvas
    global IMAGE
    sizeimage = Image.open(attrs[list(attrs.keys())[0]][0])
    img = Image.new(size = (sizeimage.size[0], sizeimage.size[1]), mode="RGBA")
    for i in attrs.values():
        pick = choice(i)
        overlap = Image.open(pick)
        overlap = overlap.convert("RGBA")
        img.paste(overlap, (0,0), mask = overlap)
    
    IMAGE = img
    show(img)
    
    print("haha")

def save():
    file = fd.asksaveasfilename(defaultextension = ".png", filetypes = (("Image", "*.png"), ))
    IMAGE.save(file)
IMAGE = None
attrs = dict()
root.title("Ama hi")
root.geometry('600x650')
root.resizable(width=False, height=False)
canvas = Canvas(root, width = 600, height = 600)
types = ttk.Combobox(root, state="readonly", values = ["Add new"] + list(attrs.keys()), font = ("Courier", 14))
types.set("Add new")
add_elements = Button(root, text = "Add", command=add, font = ("Courier", 14))
delete_elements = Button(root, text = "Delete", command=delete, font = ("Courier", 14))
generate_ = Button(root, text = "Generate", command=generate, font = ("Courier", 14))
save_ = Button(root, text = "Save", command=save, font = ("Courier", 14))
#generate.grid(column=3, row=0)
# types.grid(column=0, row=0)
# add_elements.grid(column=1, row=0)
# delete_elements.grid(column=2, row=0)
# canvas.grid(column = 0, columnspan = 100, row = 1)


canvas.pack(side = TOP, expand=True, fill=BOTH)
types.place(x = 5+107, y = 5, width = 120)
add_elements.place(x = 5+120+5+107, width = 50)
delete_elements.place(x = 5+120+5+50+5+107, width = 80)
generate_.place(x = 5+120+5+50+5+80+5+107, width = 120)
save_.place(x = (600-100)//2, y = 600-20, width = 100)
item1 = canvas.create_rectangle(30, 40, 600-30, 600-30,
                outline="grey82", fill="grey82")

def show(img):
    global canvas
    img = img.resize(((600-30-30), int(img.size[1]*(600-30-30)/img.size[0])))
    img = img.crop((0, 0, (600-30-30), (600-30-40)))
    #img.show()
    #print(img.mode)
    result = ImageTk.PhotoImage(image = img)
    canvas.image = result
    canvas.create_image((30, 40), image = result, anchor = NW)

root.mainloop()