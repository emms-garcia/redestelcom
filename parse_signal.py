#!/usr/bin/python
import sys
import os


fn = 'tmp.dat'
interface_name = 'wlan0'
keys = ['address', 'channel', 'frequency', 'quality', 'encryptionkey', 'essid' ]
routers = {}
while len(routers) < 5:
	os.system('iwlist %s scan > %s'%(interface_name, fn))
	routers = {}
	data = {}
	f = open(fn, 'r')
	for line in f.readlines():
		line = line.replace(" ", "")
		line = line.replace('"', "")
		line = line.replace("\n", "")
		line = line.lower()
		for key in keys:
			if key in line:
				if key == 'channel' and 'frequency' in line:
					pass
				else:
					if key == 'quality':
						a, q, signal = line.split("=")
						q = q.replace("signallevel", "")
						print "Qualitiy: %s"%q
						print "Signal %s"%signal
						data['quality'] = q
						data['signal'] = signal
					elif key == 'frequency':
						result, tmp = line.split('ghz')
						tmp, result = result.split(":")
						data['frequency'] = result
						print "Frequency %s GHz"%result	
					else:
						result = line.split(key)[1][1:]
						print "%s: %s"%(key, result)
						if key == 'essid':
							print result
							print ""
							routers[result] = data
							data = {}
						else:
							data[key] = result
					 
print routers
			













