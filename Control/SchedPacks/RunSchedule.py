from tkinter import ttk
import time

from Control.SchedPacks.Schedule_A import schedule_A

def second_exe(canvas):
    time.sleep(5)
    a = schedule_A()
    print(a)
    ttk.Label(canvas, text='27',width=4, relief='ridge').grid(row=7,column=9)
    print("on atteint la seconde fonction")
