#!/usr/bin/env python
# -*-coding:Latin-1 -*

import 	wiringpi2 	as 		wPi
from 	time 		import 	sleep
from 	random 		import 	randint

# Import customs class
from 	Display 	import 	*
from 	Led 		import 	*

# Set const
IN = 0
OUT = 1

UP = 1
DOWN = 0

class Shift:
	# Define wPi GPIO
	SER = 0		# Valeur
	RCLK = 0	# Validateur
	SRCLK = 0	# Suivant

	display = 0
	leds = [Led(), Led(), Led(), Led(), Led()]

	array = [[0, 0, 0],
			 [0, 0, 0],
			 [0, 0, 0],
			 [0, 0, 0],
			 [0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0]]

	def __init__(self, SER = 7, RCLK = 9, SRCLK = 8):
	#def __init__(self, SER = 1, RCLK = 16, SRCLK = 15):
		self.SER = SER
		self.RCLK = RCLK
		self.SRCLK = SRCLK

		wPi.wiringPiSetup()

		wPi.pinMode(self.SER, OUT)
		wPi.pinMode(self.RCLK, OUT)
		wPi.pinMode(self.SRCLK, OUT)

		self.loadDisplay()
		self.loadLeds()
		#self.leds = [0, 0, 0, 0, 0]

## LOADING ##
	def loadLeds(self):
		self.leds = [Led(), Led(), Led(), Led(), Led()]

		print "Leds initialized!"

	def loadDisplay(self):
		self.display = Display()
		self.clearDisplay()

		print "Display initialized!"

	def addLed(self, position, led):
		self.leds[position] = led

## SETTING LEDs COLORS ##

	## One LED ##
	def setLedColor(self, led, color, state):
		if color == 'r' or color == 'red':
			self.setLedR(led, state)
		elif color == 'g' or color == 'green':
			self.setLedG(led, state)
		elif color == 'b' or color == 'blue':
			self.setLedB(led, state)	

	def setLedColors(self, led, r, g, b):
		self.leds[led].setColors(r, g, b)

	def setLedR(self, led, r):
		self.leds[led].setR(r)

	def setLedG(self, led, g):
		self.leds[led].setG(g)

	def setLedB(self, led, b):
		self.leds[led].setB(b)

	def toggleLed(self, led):
		self.leds[led].toggleAll()

	def toggleLedColor(self, led, color):
		self.leds[led].toggleColor(color)
		self.apply()

	def applyLedColors(self, led):
		self.array[led] = self.leds[led].getColors()

	## All LEDs ##
	def setLedsColors(self, r, g, b):
		for i in range(0, 5):
			self.leds[i].setColors(r, g, b)

	def setLedsR(self, state):
		for i in range(0, 5):
			self.leds[i].setR(state)

	def setLedsG(self, state):
		for i in range(0, 5):
			self.leds[i].setG(state)

	def setLedsB(self, state):
		for i in range(0, 5):
			self.leds[i].setB(state)

	def toggleLeds(self):
		for i in range(0, 5):
			self.leds[i].toggleAll()

	def toggleLedsColor(self, color):
		for i in range(0, 5):
			self.leds[i].toggleColor(color)

	def applyLedsColors(self):
		for i in range(0, 5):
			self.array[4-i] = list(self.leds[i].getColors())

## SETTING DISPLAY ##

	def setNumber(self, x):
		self.array[5] = self.display.getNumber(x)

		if self.array == 0:
			print "Nombre saisi incorrect!"

	def setNumbers(self):
		return self.display.getNbSelected()

	def clearDisplaye(self):
		self.array[5] = self.display.clear()

## APPLY CHANGE ##
	def apply(self):
		wPi.digitalWrite(self.RCLK, DOWN)
		
		for j in reversed(self.array[5]):
			wPi.digitalWrite(self.SRCLK, DOWN)
			wPi.digitalWrite(self.SER, j)
			wPi.digitalWrite(self.SRCLK, UP)

		for i in range(0, 5):
			for j in reversed(self.array[i]):
				wPi.digitalWrite(self.SRCLK, DOWN)
				wPi.digitalWrite(self.SER, j)
				wPi.digitalWrite(self.SRCLK, UP)

		wPi.digitalWrite(self.RCLK, UP)

## CLEAR ##
	def clearDisplay(self):
		for i in range(0, 6):
			wPi.digitalWrite(self.RCLK, DOWN)
			for j in reversed(self.array[i]):
				wPi.digitalWrite(self.SRCLK, DOWN)
				wPi.digitalWrite(self.SER, DOWN)
				wPi.digitalWrite(self.SRCLK, UP)
			#	print j,
			wPi.digitalWrite(self.RCLK, UP)
			#print ""
		print "Display cleaned!"

	def clearData(self):
		for i in range(0, 6):
			for j in reversed(self.array[i]):
				self.array[i][j] = 0
		print "Data cleaned!"

## LOADINGS EFFETCS ##
	def loading(self, color):
		self.setLedColor(0, color, 1)
		self.applyLedsColors()
		self.apply()
		sleep(0.2)

		self.setLedColor(1, color, 1)
		self.applyLedsColors()
		self.apply()
		sleep(0.2)
		
		self.setLedColor(0, color, 0)
		self.setLedColor(2, color, 1)
		self.applyLedsColors()
		self.apply()
		sleep(0.2)

		self.setLedColor(1, color, 0)
		self.setLedColor(3, color, 1)
		self.applyLedsColors()
		self.apply()
		sleep(0.2)

		self.setLedColor(2, color, 0)
		self.setLedColor(4, color, 1)
		self.applyLedsColors()
		self.apply()
		sleep(0.2)

		self.setLedColor(3, color, 0)
		self.applyLedsColors()
		self.apply()
		sleep(0.2)

		self.setLedColor(4, color, 0)
		self.applyLedsColors()
		self.apply()
		sleep(0.2)

	def trimble(self):
		#self.clearData()
		#self.apply()
		color = ['r', 'g', 'b']
		for i in range(0, 3):
			print 'Set ' + str(0) + ' to ' + str(1)
			print ''
			self.setLedColor(0, color[i], 1)
			self.setNumber(randint(0, 6))
			self.applyLedsColors()
			self.apply()
			sleep(0.1)
			self.setNumber(randint(0, 6))
			self.apply()
			sleep(0.1)

			print 'Set ' + str(1) + ' to ' + str(1)
			print ''
			self.toggleLedColor(1, color[i])
			self.setNumber(randint(0, 6))
			self.applyLedsColors()
			self.apply()
			sleep(0.1)
			self.setNumber(randint(0, 6))
			self.apply()
			sleep(0.1)

			for j in range(2, 5):
				print 'Set ' + str(j-2) + ' to ' + str(0)
				print 'Set ' + str(j) + ' to ' + str(1)
				print ''
				self.toggleLedColor(j-2, color[i])
				self.toggleLedColor(j, color[i])
				self.setNumber(randint(0, 6))
				self.applyLedsColors()
				self.apply()
				sleep(0.1)
				self.setNumber(randint(0, 6))
				self.apply()
				sleep(0.1)

			print 'Set ' + str(3) + ' to ' + str(0)
			print ''
			self.toggleLedColor(3, color[i])
			self.setNumber(randint(0, 6))
			self.applyLedsColors()
			self.apply()
			sleep(0.1)
			self.setNumber(randint(0, 6))
			self.apply()
			sleep(0.1)

			print 'Set ' + str(4) + ' to ' + str(0)
			self.toggleLedColor(4, color[i])
			self.setNumber(randint(0, 6))
			self.applyLedsColors()
			self.apply()
			sleep(0.1)
#