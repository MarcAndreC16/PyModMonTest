from tkinter import ttk
import time

from Control.SchedPacks.RunSchedule import second_exe


def execute(canvas,text,master):
    print(text)
    
    ttk.Label(canvas, text='15',width=4, relief='ridge').grid(row=5,column=8)
    master.after(5000,second_exe(canvas))
    

#execute('hello world')

