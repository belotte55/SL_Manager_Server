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
# gpio = []
	
# simple_press_action = []
# double_press_action = []
# long_press_action = []

for i in range(0, 5):
	pedal = "/Root/Pedal_" + str(i) + "/"
	
#	gpio.append(int(xml.get(pedal + "GPIO")))

#	simple_press_action.append(int(xml.get(pedal + "Actions/Simple_Press")))
#	double_press_action.append(int(xml.get(pedal + "Actions/Double_Press")))
#	long_press_action.append(int(xml.get(pedal + "Actions/Long_Press")))

	pedals.append(Pedal(i, 
						int(xml.get(pedal + "GPIO")),
						int(xml.get(pedal + "Actions/Simple_Press")), 
						int(xml.get(pedal + "Actions/Double_Press")),
						int(xml.get(pedal + "Actions/Long_Press")), 
						shift, 
						sooper))
	pedals[i].start()

sooper.set_connection(str(xml.get_ip_client()), int(xml.get_port_client()))
# gpio = [24, 19, 18, 16, 15]
# simple_press_action = [18, 19, 20, 29, 4]
# double_press_action = [5, 6, 7, 8, 9]
# long_press_action   = [9, 9, 9, 9, 9]

thread = Save(xml)
thread.start()

def save_data():
	xml.write()
	print 'saved'
	sys.exit(0)

while True:
	try:
		d = s.recvfrom(1024)
		data = d[0].split()
		addr = d[1]

		print str(addr)
		
		if data:
			print str(data)

			if data[0] == 'Connection':
				#for pedal in pedals:
				sooper.set_connection(addr[0], data[1])
				xml.set_ip_client(addr[0])
				xml.set_port_client(str(data[1]))
				print 'Connected'

			elif data[0] == 'Set_All':
				for i in range(0, 5):
					pedal = "/Root/Pedal_" + str(i) + "/"

					simple_ = int(data[1 + i*3])
					double_ = int(data[1 + i*3+1])
					long_ = int(data[1 + i*3+2])

					xml.set(pedal + "Actions/Simple_Press", simple_)
					xml.set(pedal + "Actions/Double_Press", double_)
					xml.set(pedal + "Actions/Long_Press", long_)

					pedals[i].set_actions(simple_, double_, long_)
					print str(simple_) + str(double_) + str(long_)
			elif data[0] == 'Set':
				xml.set("Pedal_" + data[1] + "/Actions/" + data[2], data[3])
				pedals[int(data[1])].set_action(data[2], int(data[3]))
			elif data[0] == "Reboot":
				save_data()
				os.popen("sudo reboot")
			elif data[0] == "Halt":
				save_data()
				os.popen("sudo halt")
	except KeyboardInterrupt:
		save_data()
		sys.exit(0)
	# except KeyboardInterrupt:
	# 	save_data()
	# 	sys.exit(0)
		# elif data[0] == 'Set_Client':
		# 	xml.set("/Root/Connection/IP_Client", data[1])
		# 	xml.set("/Root/Connection/Port_Client", data[2])

		# 	for i in range(0, 5):
		# 		pedals[i].setConnection(data[1], int(data[2]))
		# elif data[0] == "Set_Port":
		# 	xml.set("/Root/Connection/Port_Client", data[1])

		# 	for i in range(0, 5):
		# 		pedals[i].setPort(int(data[1]))
#                                                                                                                                                                                                  
#                                                                                                                        
                                                                                                                                                       