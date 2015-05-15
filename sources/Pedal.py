#!/usr/bin/env python

import threading
import time
import subprocess
import socket
import RPIO

from SooperLooper import *
from Shift import *

RPIO.setmode(RPIO.BOARD)

## GLOBALS VARIABLES ##
global IN
global OUT

IN = 0
OUT = 1

global UP
global DOWN

UP = 2
DOWN = 0

## CLASS DEFINITION ##

class Pedal(threading.Thread):
	## Static variable
	currentLoop = 0
	nbOfLoops = 1
	target = ('', 0)
	
	## Init
	def __init__(self, button_id, gpio, simple_press_action, double_press_action, long_press_action, shift, sooper):
		threading.Thread.__init__(self)
		self.gpio = gpio
		self.simple_press_action = simple_press_action
		self.double_press_action = double_press_action
		self.long_press_action  = long_press_action
		self.id = button_id

		self.shift = shift
		self.sooper = sooper

		self.is_long_press = False
		self.counter = 0

		self.go_to_value = 0

		RPIO.setwarnings(False)

		RPIO.setup(self.gpio, RPIO.IN, pull_up_down = RPIO.PUD_UP)

		self.shift.setNumber(Pedal.currentLoop+1)
		self.shift.apply()

	## Called when button change state
	def is_pressing(self, channel, state):
		#if i == 0:
		#	print 'is falling'
		#elif i == 1:
		#	print 'is rising'
		
		self.counter += 1
		
		#if is falling
		if state == 0:
			# waiting for another change of state during 0.3s (simplePress|longPress)
			time.sleep(0.5)
			#print str(self.counter)
			# self.counter is incremented at each press
			# if state didn't change since the first press
			if self.counter == 1:
				# is the beginning of a Long Press
				print 'Begin long press..'

				# set is_long_press flag to True
				self.is_long_press = True

				if self.long_press_action != -1:		
					# turn up red led
					self.shift.setLedR(self.id, 1)

					self.shift.applyLedColors(self.id)
					self.shift.apply()

					# sending long_press_action to SooperLooper
					self.sooper.sendCmd(Pedal.currentLoop, self.long_press_action)
					print 'Sended...'
					#print 'Loop Selected: ' + str(Pedal.currentLoop)
		#else if is rising
		if state == 1:
			# if is_long_press
			if self.is_long_press:
				# then is it end
				print 'Ending long press!\n'

				# set is_long_press flag to False
				self.is_long_press = False

				# set self.counter to 0
				self.counter = 0

				if self.long_press_action != -1:
					
					# turn down red led
					self.shift.setLedR(self.id, 0)
					self.shift.applyLedColors(self.id)
					self.shift.apply()
					# sending long_press_action to SooperLooper
					self.sooper.sendCmd(Pedal.currentLoop, self.long_press_action)
					#print 'Loop Selected: ' + str(Pedal.currentLoop)
					self.counter = 0
			# elif is not longPress
			else:
				# waiting for another change of state during 0.5s (simplePress|doublePress)
				time.sleep(0.3)

				# if self.counter == 2 (falling + rising)
				if self.counter == 2:
					# is Simple Press
					print 'Simple Press\n'
					self.counter = 0

					if self.simple_press_action != -1:
						# turn up blue led
						self.shift.toggleLedColor(self.id, 'b')
						self.shift.applyLedColors(self.id)
						self.shift.apply()

						if self.simple_press_action == 26:
							self.add_to_current_loop(1)
						elif self.simple_press_action == 27:
							self.add_to_current_loop(-1)
						else:
							if self.simple_press_action == 28:
								Pedal.nbOfLoops += 1
							elif self.simple_press_action == 29:
								Pedal.nbOfLoops -= 1
							# sending simple_press_action to SooperLooper
							self.sooper.sendCmd(Pedal.currentLoop, self.simple_press_action)
							#print 'Loop Selected: ' + str(Pedal.currentLoop)

						time.sleep(0.5)

						self.shift.toggleLedColor(self.id, 'b')
						self.shift.applyLedColors(self.id)
						self.shift.apply()
				#if self.counter > 2 (multiple falling + rising)
				elif self.counter > 2:
					# is Double Press
					print 'Double Press\n'
					self.counter = 0

					if self.double_press_action != -1:
						# turn up green led
						self.shift.toggleLedColor(self.id, 'g')
						self.shift.applyLedColors(self.id)
						self.shift.apply()

						if self.double_press_action == 26:
							self.add_to_current_loop(1)

						elif self.double_press_action == 27:
							self.add_to_current_loop(-1)
						else:
							if self.double_press_action == 28:
								Pedal.nbOfLoops += 1
								self.add_to_current_loop(1)
							elif self.double_press_action == 29:
								Pedal.nbOfLoops -= 1
								self.add_to_current_loop(-1)
							# sending double_press_action to SooperLooper
							self.sooper.sendCmd(Pedal.currentLoop, self.double_press_action)
							#print 'Loop Selected: ' + str(Pedal.currentLoop)

						time.sleep(0.5)

						self.shift.toggleLedColor(self.id, 'g')
						self.shift.applyLedColors(self.id)
						self.shift.apply()
				#set self.counter to 0
		self.counter = 0

		# apply led changes

	## Setting actions 
	def set_action(self, press, action):
		new_action = action

		if new_action >= 1000:
			new_action = 20
			self.set_go_to_value(action - 1000)

		if press == "Simple_Press":
			self.simple_press_action = new_action
		elif press == "Double_Press":
			self.double_press_action = new_action
		elif press == "Long_Press":
			self.long_press_action = new_action

	def set_go_to_value(self, go_to_value):
		self.go_to_value = go_to_value

	def set_actions(self, simple_press_action, double_press_action, long_press_action):
		if simple_press_action >= 1000:
			self.simple_press_action = 20
			self.set_go_to_value(simple_press_action - 1000)
		else:
			self.simple_press_action = simple_press_action

		if double_press_action >= 1000:
			self.double_press_action = 20
			self.set_go_to_value(double_press_action - 1000)
		else:
			self.double_press_action = double_press_action

		if long_press_action >= 1000:
			self.long_press_action = 20
			self.set_go_to_value(long_press_action - 1000)
		else:
			self.long_press_action = long_press_action

	def add_to_current_loop(self, toAdd):
		Pedal.currentLoop += toAdd

		if Pedal.currentLoop >= Pedal.nbOfLoops:
			Pedal.currentLoop -= Pedal.nbOfLoops
		elif Pedal.currentLoop < 0:
			Pedal.currentLoop += Pedal.nbOfLoops

		self.shift.setNumber(Pedal.currentLoop+1)
		self.shift.apply()

	## Thread run
	def run(self):
		# add interrupt callback calling self.is_pressing
		RPIO.add_interrupt_callback(self.gpio, self.is_pressing, debounce_timeout_ms=10)
		# active thread for interrupts
		RPIO.wait_for_interrupts(threaded=True)