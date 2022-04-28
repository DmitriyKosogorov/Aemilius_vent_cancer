import tkinter as tk
import re
#from tkinter import Menu

import time

from blodiator.etc import coloredtext
from blodiator import blodiatorbase


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'Blodiator: '
commands=[]


#1000 1000 1450 1200
#400 600 550 500
WINDOW_MARGIN = 25  # windows extra size margin (accounted for scrollbar width)
WIDTH = 1400  # canvas width
HEIGHT = 800  # canvas height

def load_file():
    TestApp.keyPressed_im('r')
    commands=TestApp.load_commands()
    add_com_list.delete(0,tk.END)
    for command in commands:
        add_com_list.insert(tk.END,command)
    
    
def save_file():
    TestApp.keyPressed_im('w')

def add_start_node():
    TestApp.set_block_type('Source')
    TestApp.keyPressed_im('b')
    #TestApp.keyPressed_im('m')

def blocks(a=0):
    TestApp.keyPressed_im('l')

def add_mid_node():
    if(TestApp.get_block_type()=="value"):
        val=""
        toplevel=tk.Toplevel(root)
        
        def changeval(newval):
            val=newval
            if(val!=""):
                TestApp.keyPressed_im('b',val)
                #toplevel.destoy()
        
        l2 = tk.Label(toplevel, text = "choose value")
        val_entry = tk.Entry(toplevel)
        val_btn=tk.Button(toplevel, text="choose", command=lambda *args: changeval(val_entry.get()))
        l2.pack()
        val_entry.pack()
        val_btn.pack()
    elif(TestApp.get_block_type()=="command"):
        command=""
        toplevel=tk.Toplevel(root)
        
        def changecom(newcom):
            command=newcom
            if(command!=""):
                command=command.replace("> <",">,<")
                command=command.replace("><",">,<")
                commands.append(command)
                add_com_list.insert(tk.END,command)
                TestApp.keyPressed_im('b',command)
                #toplevel.destoy()
        
        l2 = tk.Label(toplevel, text = "choose command")
        val_entry_com = tk.Entry(toplevel)
        val_btn_com=tk.Button(toplevel, text="choose", command=lambda *args: changecom(val_entry_com.get()))
        l2.pack()
        val_entry_com.pack()
        val_btn_com.pack()
    else:
        TestApp.keyPressed_im('b')

def build_code():
    for i in range(5):
        print()
    with open('code.py','w') as file:
        file.write(TestApp.build_code(commands))
    print(TestApp.build_code(commands))

    
def remove_current(a=0):
    TestApp.keyPressed_im('d')

CT = coloredtext.ColoredText()

CT.Print('Starting Blodiator', fg, bg, style, 'Root: ')

root = tk.Tk()
root.geometry("{0}x{1}".format(WIDTH + WINDOW_MARGIN, HEIGHT + WINDOW_MARGIN))
root.title('Blodiator Base Test Bench')
mainmenu = tk.Menu(root)
root.config(menu=mainmenu) 
filemenu = tk.Menu(mainmenu)
filemenu.add_command(label="Загрузить",command=load_file)
filemenu.add_command(label="Сохранить",command=save_file)
mainmenu.add_cascade(label="Файл", menu=filemenu)
buttons=[]
button_add=tk.Button(root, text ="add start block", command = add_start_node, height = 10, width = 20)
button_add.grid(row=0,column=0)
button_add_mid=tk.Button(root, text ="add chosen block", command = add_mid_node, height = 10, width = 20)

button_add_end=tk.Button(root, text ="build code", command = build_code, height = 10, width = 20)

button_remove=tk.Button(root, text ="delete block", command = remove_current, height = 10, width = 20)

#add_one.pack(side = tk.LEFT, pady = 0)
TestApp = blodiatorbase.BlodiatorBase(master=root, std=CT,size=(800,600),grid=(0,1,7,7))
root.bind('<Button-3>',blocks)
root.bind('<Delete>', remove_current)
add_com_text = tk.Label(root, text='Add command')
add_com_text.grid(row=0,column=8, columnspan=3)
add_com_entry = tk.Entry(root)
add_com_entry.grid(row=1,column=8, columnspan=3)
add_com_list = tk.Listbox(root)
add_com_list.grid(row=3, column=8,columnspan=3)

def add_command():
    commands.append(add_com_entry.get())
    add_com_list.insert(tk.END,add_com_entry.get())

add_com_button=tk.Button(root, text='add command', command=add_command)

button_add_mid.grid(row=1,column=0)
button_remove.grid(row=3,column=0)
add_com_button.grid(row=2,column=8, columnspan=3)
button_add_end.grid(row=2,column=0)
root.mainloop()


CT.Print('Closing Blodiator', fg, bg, style, 'Root: ')  

