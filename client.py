#!usr/bin/python
import sys
import Tkinter as tk
import time
import socket

#Funcion llamada cuando se presiona cualquier boton
#Parametros
#-string cadena de texto que representa el boton presionado
def callback(string):
	s.sendto(string.decode('hex'), (UDP_IP, port))
	time.sleep(0.2)

if __name__ == "__main__":
	host = sys.argv[1] #nombre identificador del cliente
	port = int(sys.argv[2]) #numero de puerto al cual se realizara la conexion
	UDP_IP = '127.0.0.1'
	PACKET_DATA = 'f1a525da11f6'.decode('hex')
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.sendto(PACKET_DATA, (UDP_IP, port))
	data, addr = s.recvfrom(1024)
	if data:
		print "Conexion exitosa."
	else:
		print "No se pudo conectar con %s."%UDP_IP
		sys.exit()
	root = tk.Tk() #creacion de la ventana donde se colocaran los botones
	root.title("Cliente de %s"%host) #titulo de la ventana
	#Canvas usado como contenedor para los botones, pintado dependiendo del cuadro
	#que mueve el cliente
	canvas = tk.Canvas(root, width = 200, height = 200, background = data)
	#Inicializacion de botones
	button = tk.Button(canvas, text = 'Up', command = lambda:callback('A1'), width = 10)
	button_window = canvas.create_window(100, 10, anchor='n', window=button)
	button = tk.Button(canvas, text = 'Down', command = lambda:callback('B1'), width = 10)
	button_window = canvas.create_window(100, 90, anchor='n', window=button)
	button = tk.Button(canvas, text = 'Left', command = lambda:callback('C1'), width = 10)
	button_window = canvas.create_window(50, 50, anchor='n', window=button)
	button = tk.Button(canvas, text = 'Right', command = lambda:callback('D1'), width = 10)
	button_window = canvas.create_window(150, 50, anchor='n', window=button)
	canvas.pack()
	root.mainloop()

