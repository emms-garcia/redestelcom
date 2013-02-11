import Tkinter as tk
import random
from sys import argv
import socket, thread
import numpy

#Clase encargada de dibujar los rectangulos, guardar sus coordenadas, y moverlos.
#Parametros
#-(x, y) Tupla de coordenadas dentro del grid
#-color Color del rectangulo a generar
class Rectangle(object):
	def __init__(self, (x, y), color):
		grid.matrix[x, y] = 2
		self.x = x
		self.y = y
		self.color = color
		self.rect = None
		self.canvas = None

	def draw(self, canvas, n, m):
				self.canvas = canvas
				self.rect = canvas.create_rectangle(0 + (n*self.x), 0 + (m*self.y), n + (n*self.x), m + (m*self.y), fill = self.color)

	def move(self, direction):
		UP = 'A1'.decode('hex')
		DOWN = 'B1'.decode('hex')
		LEFT = 'C1'.decode('hex')
		RIGHT = 'D1'.decode('hex')
		if direction == UP:
			x, y = 0, -1
		elif direction == LEFT:
			x, y = -1, 0
		elif direction == DOWN:
			x, y = 0, 1
		elif direction == RIGHT:
			x, y = 1, 0
		if grid.is_valid(self.x + x, self.y + y):
			grid.matrix[self.x, self.y] = 0
			self.x += x
			self.y += y
			grid.matrix[self.x, self.y] = 2
			w, h = int(self.canvas.cget('width')), int(self.canvas.cget('height'))
			n = w/len(grid.matrix)
			m = h/len(grid.matrix[0])
			self.canvas.coords(self.rect,  0 + (n*self.x), 0 + (m*self.y), n + (n*self.x), m + (m*self.y))
			return True
		else:
			return False

	def update(self, (x, y)):
		grid.matrix[self.x, self.y] = 0
		self.x = x
		self.y = y
		grid.matrix[self.x, self.y] = 0
		n = w/len(grid.matrix)
		m = h/len(grid.matrix[0])
		self.canvas.coords(self.rect,  0 + (n*self.x), 0 + (m*self.y), n + (n*self.x), m + (m*self.y))
		return

#Clase encargada de crear el grid a partir de una matriz con ceros y unos, dibujarla en el canvas
#y ademas verificar movimientos validos para los rectangulos
#Parametros
#-n largo de la matriz
#-m ancho de la matriz
class Grid:
	def __init__(self, n, m):
		self.n = n
		self.m = m
		self.matrix = self.init_matrix(n, m)

	def init_matrix(self, n, m):
		matrix = numpy.zeros((n,m), dtype = numpy.int8)
		for i in range(len(matrix)):
			for j in range(len(matrix[i])):
				if i == 0 or j == 0 or i == len(matrix)-1 or j == len(matrix[i]) - 1:
					matrix[i, j] = 1
		return matrix

	def draw_matrix(self, canvas, w, h):
		n = len(self.matrix)
		m = len(self.matrix[0])
		div_x = w/n
		div_y = h/m
		for i in range(n):
			for j in range(m):
				if self.matrix[j, i] == 1:
					canvas.create_rectangle(0 + (i*div_x), 0 + (j*div_y), div_x + (i*div_x), div_y + (j*div_y), fill = "gray")
				else:
					canvas.create_rectangle(0 + (i*div_x), 0 + (j*div_y), div_x + (i*div_x), div_y + (j*div_y), fill = "blue")
		canvas.update()
		return div_x, div_y

	def is_valid(self, x, y):
		if self.matrix[x, y] == 1 or self.matrix[x, y] == 2:
			return False
		else:
			return True

#Clase que se ocupa de manejar las conexiones entre el servidor y los clientes
#y la recepcion de la informacion de parte de los mismos.
class Server:
	def __init__(self):
		self.clients = {}
		self.UDP_IP = '127.0.0.1'
		self.hostnames = {}
		self.act = 0
		port = int(argv[1])
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((self.UDP_IP, int(argv[1])))
		thread.start_new_thread(self.listen_connections,(s, ))
		
	def listen_connections(self, conn):
		global colors
		PACKET_DATA = 'f1a525da11f6'.decode('hex')
		while True:
			data, addr = conn.recvfrom(1024)
			if PACKET_DATA == data:
				print 'Cliente %s, %s conectado.'%(addr)
				conn.sendto(colors[self.act], addr)
			else:
				players[self.clients[addr]].move(data)
			if addr not in self.clients:
				self.clients[addr] = colors[self.act]
				self.act += 1
		

def generate_pair(xlimit, ylimit):
	x, y = 0, 0
	while not grid.is_valid(x, y):
		x, y = random.randint(0, xlimit), random.randint(0, ylimit)
	return x, y
	
if __name__ == "__main__":
	colors = ['red', 'green'] #colores a asignar a los clientes entrantes
	w, h = 600, 600 #ancho y largo de la ventana
	grid = Grid(10, 10) #grid de accion del "juego"
	players = {} #diccionario para guardar los objetos de los jugadores
	s = Server() #creacion de un servidor para manejar la conexion con sockets
	root = tk.Tk() #ventana para mostrar el "juego"
	root.title('Servidor')
	canvas = tk.Canvas(root, width = w, height = h)
	n, m = grid.draw_matrix(canvas, w, h)
	x, y = generate_pair(len(grid.matrix)-1, len(grid.matrix[0])-1)
	players['red'] = Rectangle((x, y), "red")
	players['red'].draw(canvas, n, m)
	x, y = generate_pair(len(grid.matrix)-1, len(grid.matrix[0])-1)
	players['green'] = Rectangle((x, y), "green")
	players['green'].draw(canvas, n, m)
	canvas.pack()
	root.mainloop()
