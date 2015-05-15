#!/usr/bin/env python
# -*-coding:Latin-1 -*

import wiringpi2 as wPi
from time import sleep

class Display:
	numbers =  [[0, 1, 1, 1, 0, 1, 1, 1],	# 0
				[0, 0, 0, 1, 0, 1, 0, 0],	# 1
				[1, 0, 1, 1, 0, 0, 1, 1],	# 2
				[1, 0, 1, 1, 0, 1, 1, 0],	# 3
				[1, 1, 0, 1, 0, 1, 0, 0],	# 4
				[1, 1, 1, 0, 0, 1, 1, 0],	# 5
				[1, 1, 1, 0, 0, 1, 1, 1],	# 6
				[0, 0, 1, 1, 0, 1, 0, 0],	# 7
				[1, 1, 1, 1, 1, 1, 1, 1],	# 8
				[1, 1, 1, 1, 0, 1, 1, 0],	# 9
				[0, 0, 0, 0, 0, 0, 0, 0]]	# Clear

	nbSelected = -1

	def __init__(self):
		for i in range(0, 11):
			#self.numbers[i].reverse()
			pass	

	def getNumber(self, x):
		self.nbSelected = x
		return self.numbers[self.nbSelected]

	def getNbSelected(self):
		return self.nbSelected

	def clear(self):
		self.nbSelected = 10

		return self.numbers[self.nbSelected]
#