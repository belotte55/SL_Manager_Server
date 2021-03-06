#!/usr/bin/env python
# -*-coding:Latin-1 -*

import wiringpi2 as wPi
from time import sleep

class Led:
	R = 0
	G = 0
	B = 0
	
	def __init__(self):
		self.R = 0
		self.G = 0
		self.B = 0

	def setColors(self, r, g, b):
		self.R = r
		self.G = g
		self.B = b

	def setR(self, r):
		self.R = r

	def setG(self, g):
		self.G = g

	def setB(self, b):
		self.B = b

	def getColors(self):
		#print self.R, self.G, self.B
		return (self.R, self.G, self.B)

	def toggleAll(self):
		self.R = not self.R
		self.G = not self.G
		self.B = not self.B

	def toggleColor(self, color):
		if color == 'r' or color == 'red':
			self.R = not self.R
		elif color == 'g' or color == 'green':
			self.G = not self.G
		elif color == 'b' or color == 'blue':
			self.B = not self.B

#                                             