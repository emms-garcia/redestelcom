#!usr/bin/python
from socket import *
from sys import argv
import Tkinter as tk
import time

def callback(string):
	print string
	s.send(string)
	time.sleep(0.5)

port = int(argv[2])
host = argv[1]

s = socket()
s.connect(('', port)) 
s.send(host)

data = s.recv(1024)
print data
time.sleep(0.5)
color = s.recv(1024)
color = color.replace("<color>", "")
root = tk.Tk()
root.title(host)

canvas = tk.Canvas(root, width = 200, height = 200, background = color)
button = tk.Button(canvas, text = 'Up', command = lambda:callback('up'), width = 10)
button_window = canvas.create_window(100, 10, anchor='n', window=button)
button = tk.Button(canvas, text = 'Down', command = lambda:callback('down'), width = 10)
button_window = canvas.create_window(100, 90, anchor='n', window=button)
button = tk.Button(canvas, text = 'Left', command = lambda:callback('left'), width = 10)
button_window = canvas.create_window(50, 50, anchor='n', window=button)
button = tk.Button(canvas, text = 'Right', command = lambda:callback('right'), width = 10)
button_window = canvas.create_window(150, 50, anchor='n', window=button)
canvas.pack()


root.mainloop()


#s.close()

