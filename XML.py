#!/usr/bin/env python
# -*- coding: utf-8 -*-

# By Frederic Henner #

from lxml import etree
import xml.etree.ElementTree as ET


## CLASS DEFINITION ##
class XML():
	
	## Init
	def __init__(self,file):
		self.treeParse = ""
		self.file = file

		self.parsing_xml()	

	## Parsing XML
	def parsing_xml(self):
		self.treeParse = etree.parse(self.file)
		print "Le fichier est parsé"

	## Reading IP Address
	def get_ip_client(self):
		#for gIP in self.treeParse.xpath("/Root/Connection/IP_Client"):
		return self.treeParse.xpath("/Root/Connection/IP_Client")[0].text

	## Reading PORT
	def get_port_client(self):
		return self.treeParse.xpath("/Root/Connection/Port_Client")[0].text

	def get_port_server(self):
		return self.treeParse.xpath("/Root/Connection/Port_Server")[0].text

	## Writing IP Address
	def set_ip_client(self, ip):
		self.treeParse.xpath("/Root/Connection/IP_Client")[0].text = ip

	## Writing PORT
	def set_port_client(self, port):
		self.treeParse.xpath("/Root/Connection/Port_Client")[0].text = port

	def set_port_server(self, port):
		self.treeParse.xpath("/Root/Connection/Port_Server")[0].text = port

		## Reading Other XML
	def get(self,path):
		return self.treeParse.xpath(path)[0].text

	## Writing Other XML
	def set(self, path, value):	
		self.treeParse.xpath(path)[0].text = value

	## Write the file
	def write(self):	
		self.treeParse.write(self.file)	

	# ## Reading Pedal without option = Actions
	# def GetPedal_O(self,numb,option):
	# 	for gPedal1 in self.treeParse.xpath("/Root/Pedal_"+numb+"/"+option):
	# 		print ("Pedal : "+gPedal1.text)

	# ## Writing Pedal witout option = Actions
	# def SetPedal_O(self,numb,option,new):
	# 	for sPedal1 in self.treeParse.xpath("/Root/Pedal_"+numb+"/"+option):
	# 		sPedal1.text=new
	# 		print ("Pedal : "+sPedal1.text)

	# ## Reading Pedal with option = Actions
	# def GetPedal_A(self,numb,option,option2):
	# 	for gPedal2 in self.treeParse.xpath("/Root/Pedal_"+numb+"/"+option+"/"+option2):
	# 		print ("Pedal : "+gPedal2.text)

	# ## Writing Pedal with option = Actions
	# def SetPedal_A(self,numb,option,option2,new):
	# 	for sPedal2 in self.treeParse.xpath("/Root/Pedal_"+numb+"/"+option+"/"+option2):
	# 		sPedal2.text = new
	# 		print ("Pedal : "+sPedal2.text)

	## Writing Default XML
	def ResetXML(self):
			# Création Pedalier 
		Root = etree.Element("Root")
			# Création Pedale 
		pedal = etree.ElementTree(Root)
		gpio = [24,19,18,16,15]
		for i in range(5):
				#Création Pedale n° i
			pedal = etree.SubElement(Root,"pedal")
				# Ajout d'un parametre i , pour la distinction
			pedal.set("number", `i`)
				# Création de la branche GPIO
			GPIO = etree.SubElement(pedal,"GPIO")
			GPIO.text = str(gpio[i])
				# Création de la branche Go_to_value
			Gtv = etree.SubElement(pedal, "Go_to_value")
			Gtv.text = "0"
				# Création de la branche Actions
			Actions=etree.SubElement(pedal, "Actions")
			SP = etree.SubElement(Actions,"Simple_Press")
			SP.text = "-1"
			DP = etree.SubElement(Actions, "Double_Press")
			DP.text = "-1"
			LP = etree.SubElement(Actions, "Long_Press")
			LP.text = "-1"
				# Création de la branche Connection
		Connection = etree.SubElement(Root, "Connection")
			# Création de la branche IP
		IP = etree.SubElement(Connection, "IP")
		IP.text = "A modifier"
			# Création de la branche PORT
		PORT = etree.SubElement(Connection, "PORT")
		PORT.text = "A modifier"
			# Write to self.file:
		self.treeParse = etree.ElementTree(Root)
		self.treeParse.write(self.file,pretty_print=True)

	## XML in Tree
	def Tree(self):
		print ("Iprojet")
		for i in range(5):
			print("-Pedal n°"+`i+1`)
			for GPIO in self.treeParse.xpath("/Root/Pedal_"+`i+1`+"/GPIO"):
				print("--Gpio "+GPIO.text)
			for GTV in self.treeParse.xpath("/Root/Pedal_"+`i+1`+"/Go_to_value"):
				print("--Go to value "+GTV.text)
			print("--Actions")
			for ACT_SP in self.treeParse.xpath("/Root/Pedal_"+`i+1`+"/Actions/Simple_Press"):
				print("---Simple_Press "+ACT_SP.text)
			for ACT_DP in self.treeParse.xpath("/Root/Pedal_"+`i+1`+"/Actions/Double_Press"):
				print("---Double_Press "+ACT_DP.text)
			for ACT_LP in self.treeParse.xpath("/Root/Pedal_"+`i+1`+"/Actions/Long_Press"):
				print("---Long_Press "+ACT_LP.text)
		print("-Connection")
		for IP in self.treeParse.xpath("/Root/Connection/IP"):
			print("--IP "+IP.text)
		for PORT in self.treeParse.xpath("/Root/Connection/PORT"):
			print("--PORT "+PORT.text)

# if __name__ == '__main__':

# 	xml = XML('Preferences.xml')

# 	gpio = []
	
# 	simple_press_action = []
# 	double_press_action = []
# 	long_press_action = []

# 	for i in range(0, 5):
# 		pedal = "/Root/Pedal_" + str(i) + "/"
		
# 		gpio.append(int(xml.get(pedal + "GPIO")))

# 		simple_press_action.append(int(xml.get(pedal + "Actions/Simple_Press")))
# 		double_press_action.append(int(xml.get(pedal + "Actions/Double_Press")))
# 		long_press_action.append(int(xml.get(pedal + "Actions/Long_Press")))

# 		print str(gpio[i]) + " - " + str(simple_press_action[i]) + " - " + str(double_press_action[i]) + " - " + str(long_press_action[i])
	#test.GetPORT()
	#test.SetIP("192.168.123.11")
	#test.SetPORT("9999")
	#test.ResetXML()
	#test.GetPedal_O("1","GPIO")
	#test.SetPedal_O("2","GPIO","GG fredo")
	#test.GetPedal_A("2","Actions","Simple_Press")
	#test.SetPedal_A("2","Actions","Simple_Press","mod pd")
	#test.XMLreading("/Root/Pedal_1]/GPIO")
	#test.XMLwriting("/Root/Pedal_1]/GPIO","mod")
	#test.Tree()

	#test.Write()