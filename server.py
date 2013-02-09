#!/usr/bin/python
import socket
import thread
from sys import argv

host = ''
port = int(argv[1])

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(3)

clients = {}
hostnames = {}


def handle_connection(conn, addr, host):
	conn.send('Cliente %s conectado al servidor.'%host)
	hostnames[conn] = host
	clients[conn] = addr
	while True:
		data = conn.recv(1024)
		for client in clients:
			if client != conn:
				client.sendto(">%s: %s"%(host, data), clients[client])

while True:
	conn, addr = s.accept()
	host = conn.recv(1024)
	thread.start_new_thread(clientthread,(conn, addr, host))

conn.close()
s.close()

