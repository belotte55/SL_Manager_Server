#!/usr/bin/python
# -*-coding:Latin-1 -*

import socket
import sys
import time
import os

from threading import Thread

#sys.path.append('/home/pi/Programmes/Python/Projet')

from Pedal import *
from SooperLooper import *
from XML import *

HOST = ''
PORT = 9000

current_ip = ''
current_port = 0

# if an argument is passed, save it as new port
if len(sys.argv) > 1:
	PORT = int(sys.argv[1])

# try to create socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error, msg:
	print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

# try to bind socket
try:
	s.bind((HOST, PORT))
	print 'Server running on port ' + str(PORT) + '.'
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

class Save(Thread):
	def __init__(self, xml):
		Thread.__init__(self)
		self.xml = xml
	
	def run(self):
		while True:
			time.sleep(300)
			self.xml.write()
			print 'Saved'

# get XML document
xml = XML('/home/pi/Programmes/Python/Projet/Preferences.xml')

# instanciate shift and sooperlooper
shift = Shift()
sooper = SooperLooper()

# animate LEDs
shift.loading('b')

# 
pedals = []

for i in range(0, 5):
	pedal = "/Root/Pedal_" + str(i) + "/"

	pedals.append(Pedal(i, 
						int(xml.get(pedal + "GPIO")),
						int(xml.get(pedal + "Actions/Simple_Press")), 
						int(xml.get(pedal + "Actions/Double_Press")),
						int(xml.get(pedal + "Actions/Long_Press")), 
						shift, 
						sooper))
	pedals[i].start()

current_ip = str(xml.get_ip_client())
current_port = int(xml.get_port_client())

sooper.set_connection(current_ip, current_port)

thread = Save(xml)
thread.start()

def save_data():
	xml.write()
	print 'saved'

while True:
	try:
		d = s.recvfrom(1024)
		data = d[0].split()
		addr = d[1]

		if addr[0] != current_ip:
			current_ip = str(addr[0])
			xml.set_ip_client(current_ip)
			sooper.set_connection(current_ip, current_port)
			print 'New ip: ' + current_ip
		
		if data:
			print 'Message received: ' + str(d[0])

			if data[0] == 'Connection':
				current_port = int(addr[1])
				xml.set_port_client(str(current_port))
				sooper.set_connection(current_ip, current_port)

				print 'New port: ' + str(current_port)

			elif data[0] == 'Set_All':
				for i in range(0, 5):
					pedal = "/Root/Pedal_" + str(i) + "/"

					simple_ = str(data[1 + i*3])
					double_ = str(data[1 + i*3+1])
					long_ = str(data[1 + i*3+2])

					xml.set(pedal + "Actions/Simple_Press", simple_)
					xml.set(pedal + "Actions/Double_Press", double_)
					xml.set(pedal + "Actions/Long_Press", long_)

					pedals[i].set_actions(int(simple_), int(double_), int(long_))
					print str(simple_) + str(double_) + str(long_)
			elif data[0] == 'Set':
				xml.set("Pedal_" + data[1] + "/Actions/" + data[2], data[3])
				pedals[int(data[1])].set_action(data[2], int(data[3]))
			elif data[0] == "Reboot":
				save_data()
				os.popen("sudo reboot")
				sys.exit(0)
			elif data[0] == "Halt":
				save_data()
				os.popen("sudo halt")
				sys.exit(0)
	except KeyboardInterrupt:
		save_data()
		sys.exit(0)
