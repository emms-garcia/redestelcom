import Tkinter as tk
import random
import ImageTk, Image
from sys import argv
import socket, thread


matrix = [ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
					[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
					[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
					[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
					[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
					[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
					[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
					[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
					[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
					[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

class Player(object):
	def __init__(self, (x, y), color):
		global matrix
		matrix[x][y] = 2
		self.x = x
		self.y = y
		self.color = color
		self.rect = None
		self.canvas = None

	def draw(self, canvas, n, m):
				self.canvas = canvas
				self.rect = canvas.create_rectangle(0 + (n*self.x), 0 + (m*self.y), n + (n*self.x), m + (m*self.y), fill = self.color)

	def move(self, (x, y)):
		global matrix
		if is_valid(self.x + x, self.y + y):
			matrix[self.x][self.y] = 0
			print 'valid'
			self.x += x
			self.y += y
			matrix[self.x][self.y] = 2
			w, h = int(self.canvas.cget('width')), int(self.canvas.cget('height'))
			n = w/len(matrix)
			m = h/len(matrix[0])
			self.canvas.coords(self.rect,  0 + (n*self.x), 0 + (m*self.y), n + (n*self.x), m + (m*self.y))
			#draw_matrix(w, h)
			return True
		else:
			print "Not valid"
			return False

	def update(self, (x, y)):
		global matrix
		matrix[self.x][self.y] = 0
		self.x = x
		self.y = y
		matrix[self.x][self.y] = 0
		n = w/len(matrix)
		m = h/len(matrix[0])
		self.canvas.coords(self.rect,  0 + (n*self.x), 0 + (m*self.y), n + (n*self.x), m + (m*self.y))
		return


def draw_matrix(w, h):
	global matrix
	n = len(matrix)
	m = len(matrix[0])
	div_x = w/n
	div_y = h/m
	for i in range(n):
		for j in range(m):
			if matrix[j][i] == 1:
				canvas.create_rectangle(0 + (i*div_x), 0 + (j*div_y), div_x + (i*div_x), div_y + (j*div_y), fill = "gray")
			else:
				canvas.create_rectangle(0 + (i*div_x), 0 + (j*div_y), div_x + (i*div_x), div_y + (j*div_y), fill = "blue")
	canvas.update()
	return div_x, div_y

def is_valid(x, y):
	global matrix
	if matrix[x][y] == 1 or matrix[x][y] == 2:
		return False
	else:
		return True

def move(pcolor, direction):
	if direction == 'up':
		players[pcolor].move((0, -1))
	elif direction == 'left':
		players[pcolor].move((-1, 0))
	elif direction == 'down':
		players[pcolor].move((0, 1))
	elif direction == 'right':
		players[pcolor].move((1, 0))

			
def clientthread(conn, addr, host):
	global act
	conn.send('Cliente %s conectado al servidor.'%host)
	clients[conn] = colors[act]
	conn.send('<color>%s'%colors[act])
	act += 1
	while True:
		data = conn.recv(1024)
		print data
		move(clients[conn], data)
		

def accept_connections(s):
	while True:
		conn, addr = s.accept()
		host = conn.recv(1024)
		thread.start_new_thread(clientthread,(conn, addr, host))
	
		
		
if __name__ == "__main__":
	colors = ['red', 'green']
	act = 0
	root = tk.Tk()
	w, h = 600, 600
	canvas = tk.Canvas(root, width = w, height = h)
	n, m = draw_matrix(w, h)
	players = {}
	x, y = 0, 0
	while not is_valid(x, y):
		x, y = random.randint(0, len(matrix)-1), random.randint(0, len(matrix[0])-1)
	players['red'] = Player((x, y), "red")
	players['red'].draw(canvas, n, m)
	x, y = 0, 0
	while not is_valid(x, y):
		x, y = random.randint(0, len(matrix)-1), random.randint(0, len(matrix[0])-1)
	players['green'] = Player((x, y), "green")
	players['green'].draw(canvas, n, m)
	canvas.pack()

	host = ''
	port = int(argv[1])

	s = socket.socket()
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((host, port))
	s.listen(3)

	clients = {}
	hostnames = {}
	thread.start_new_thread(accept_connections,(s, ))
	root.mainloop()
