#!usr/bin/python
from socket import *
from sys import argv
import thread, time

def read_input(s, host):
	while True:
		msg = raw_input(">%s: "%host)
		if msg == "exit":
			print "Conexion Terminada"
			s.close()
		else:
			s.send(msg)

port = int(argv[2])
host = argv[1]

s = socket()
s.connect(('', port)) 
s.send(host)

data = s.recv(1024)
print data
thread.start_new_thread(read_input, (s, host))

while True:
	data = s.recv(1024)
	if data != None or data != "":
		print data

s.close()

