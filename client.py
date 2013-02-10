#!usr/bin/python
from socket import *
import sys
import Tkinter as tk
import time

#Funcion llamada cuando se presiona cualquier boton
#Parametros
#-string cadena de texto que representa el boton presionado
def callback(string):
	s.send(string)
	time.sleep(0.2)

if __name__ == "__main__":
	host = sys.argv[1] #nombre identificador del cliente
	port = int(sys.argv[2]) #numero de puerto al cual se realizara la conexion

	s = socket() 
	s.connect(('', port)) #conexion del cliente al puerto proporcionado como argumento
	s.send(host)

	data = s.recv(1024) #recepcion inicial de datos para comprobar el exito de la conexion
	if data:
		print "Conexion al servidor exitosa."
	else:
		print "Falla en la conexion. Terminando..."
		s.close()
		sys.exit()
	root = tk.Tk() #creacion de la ventana donde se colocaran los botones
	root.title("Cliente de %s"%host) #titulo de la ventana
	#Canvas usado como contenedor para los botones, pintado dependiendo del cuadro
	#que mueve el cliente
	canvas = tk.Canvas(root, width = 200, height = 200, background = data)
	#Inicializacion de botones
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

