#!/usr/bin/env python
# -*-coding:Latin-1 -*

import liblo, sys
import socket

listCmd = [ 'undo',
			'redo',
			'record',
			'overdub',
			'multiply',
			'load',
			'save',
			'trigger',
			'once',
			'mute on',	#
			'solo',
			'replace',
			'substitute',
			'insert',
			'delay',
			'rev',
			'scratch',
			'pause',
			'pocket next', #18
			'pocket prev', #19
			'pocket go_to_value', # 20
			'', # loop A
			'',	# loop B
			'',	# loop C
			'',	# loop D
			'',	# loop E
			'', # next loop
			'', # prev loop
			'',	# add loop    - 28
			'',]# remove loop - 29

class SooperLooper(object):
	def __init__(self):
		self.isMuteOn = False

		self.ip = ""
		self.port = 0

		self.target = ''

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		self.initialized = False

	def sendCmd(self, loopID, cmd):
		if self.initialized:
			trame = '/sl/' + str(loopID) + '/hit'

			## spécials commands
			if cmd == 18:
				print "Pocket_Pod Next" + str(self.port)
				self.sock.sendto("Pocket_Pod Next", (self.ip, int(self.port)))
			elif cmd == 19:
				print "Pocket_Pod Prev"
				self.sock.sendto("Pocket_Pod Prev", (self.ip, self.port))
			elif cmd == 20:
				print "Pocket_Pod GoTo"
				self.sock.sendto("Pocket_Pod Go_To", (self.ip, self.port))
			
			elif cmd == 28:
				self.addLoop(loopID)
			elif cmd == 29:
				self.removeLoop()
			elif cmd == 9:
				if not self.isMuteOn:
					liblo.send(self.target, trame, 'mute_on')
					self.isMuteOn = True
				else:
					liblo.send(self.target, trame, 'mute_off')
					self.isMuteOn = False
			
			## classic command
			else:
				print 'Sending...'
				liblo.send(self.target, trame, listCmd[cmd])

	def addLoop(self, loopID):
		trame = '/loop_add'
		liblo.send(self.target, trame, loopID, 0)
		print(trame)

	def removeLoop(self):
		trame = '/loop_del'
		liblo.send(self.target, trame, -1)
		print(trame)

	def set_connection(self, ip, port):
		self.ip = ip
		self.port = int(port)

		self.target = 'osc.udp://' + self.ip + ':9951'
		self.initialized = True

	def setPort(self, port):
		self.port = port

#                                                                                                                                                                                                             