# IOT CODE **************************************************************************************
from urllib2 import urlopen, Request
from time import mktime, sleep
from datetime import datetime
from json import dumps
iotdata ="Y"
yureka_str = ""
oldmax=0
curmax = 0
String="Y"


class Client (object):
    api_url = "http://api.carriots.com/streams"

    def __init__(self, api_key=None, client_type='json'):
        self.client_type = client_type
        self.api_key = api_key
        self.content_type = "application/vnd.carriots.api.v2+%s" % self.client_type
        self.headers = {'User-Agent': 'Raspberry-Carriots',
                        'Content-Type': self.content_type,
                        'Accept': self.content_type,
                        'Carriots.apikey': self.api_key}
        self.data = None
        self.response = None

    def send(self, data):
        self.data = dumps(data)
        request = Request(Client.api_url, self.data, self.headers)
        self.response = urlopen(request)
        return self.response

def iotsend(ack):
    device = "RPI@BOTRIO.BOTRIO"
    apikey = "41d753080c1a2a72515e2fff11d116cdd8f7e91a5b3a2b278b9612af135edc71"  # Replace with your Carriots apikey
    client_carriots = Client(apikey)
    timestamp = int(mktime(datetime.utcnow().timetuple()))
    data = {"protocol": "v2", "device": device, "at": timestamp, "data": dict(
    light=ack)}
    carriots_response = client_carriots.send(data)
    print carriots_response.read()


def readfile(filename):
    global iot
    global yureka_str
    global String
    file=open(filename,"r")
    data =file.read()
    print data
    file.close()
    list = re.findall("iot[\d][\d][\d]",data)
    print list
    numlist = []
    for entry in list:
                #rint int(entry[-3:])
                numlist.append(int(entry[-3:]))
    print numlist
    curmax= max(numlist)
    if curmax < 9 :
	curmax = "00"+str(curmax)
    elif curmax > 9 and curmax <100 :
	curmax = "0"+str(curmax)
    else:
	curmax = str(curmax)	
    yureka_str = "iot"+curmax+"(.*)~"
    print yureka_str
    matches = re.findall(yureka_str,data)
    print matches
    fo=open("iotoldmax.txt","r")
    oldmax =fo.readline().strip()
    fo.close()
    fo=open("iotoldmax.txt","w")
    fo.write(str(curmax))
    fo.close()
    print "************"
    print oldmax
    print "************"
    print curmax
    print "************"

    if int(curmax) >int(oldmax):
	
	print "need correction"*100
	print curmax
	print oldmax
	ifile=open("iotdata.txt","w")
	ifile.write(matches[0])
	ifile.close()
	ffile=open("iotflag.txt","w")
	ffile.write("1")
	ffile.close()
	print "here"
        String = matches[0]
        iotsend("iot"+str(curmax)+"ACK")

    else:
        print "fail"
        String = "Y."
    print  "output"+String
def readfromcloud():
	while True:
		os.system("curl --header \"carriots.apikey:41d753080c1a2a72515e2fff11d116cdd8f7e91a5b3a2b278b9612af135edc71\" \"http://api.carriots.com/streams/?device=iPhone6Mobile@BOTRIO.BOTRIO\" > hi.txt ")
		readfile("hi.txt")
		#time.sleep(10)
#************************************************** IOT CODE **************************************************************************************
import socket
import time
import os
import sys
import serial
import threading
import re
import RPi.GPIO as GPIO
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
nflag = 0
appdata = "Y"
 
#%%%%%%%%%%%%%%%%%%% Servo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
os.system('sudo ./servod')
os.system("echo 0=50 > /dev/servoblaster")
os.system("echo 1=50 > /dev/servoblaster")
os.system("echo 2=50 > /dev/servoblaster")
os.system("echo 3=50 > /dev/servoblaster")
os.system("echo 4=50 > /dev/servoblaster")
os.system("echo 5=50 > /dev/servoblaster")
os.system("echo 6=50 > /dev/servoblaster")
os.system("echo 7=50 > /dev/servoblaster")
S1OldAngle = 0
S2OldAngle = 0
S3OldAngle = 0
S4OldAngle = 0
S5OldAngle = 0
S6OldAngle = 0
S7OldAngle = 0
S8OldAngle = 0
#%%%%%%%%%%%%%%%%%%% Servo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#@@@@@@@@@@@@@@@@ sensor @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
NoOfSensors =""
SensorPort =""  
ComparingValue = 0
LogicalOpr = ""
SensorString =  ""
TruePart = ""
FalsePart = ""
TStart = ""
TEnd = ""
FStart = "" 
FEnd = ""
#@@@@@@@@@@@@@@@@ sensor @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
usbport='/dev/ttyAMA0'
por = serial.Serial(usbport,115200,timeout=15.0)
por.flushInput()

BracketList = []
RepeatCountList = []
Bi= 0
Ri = 0
i = 0
#BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
sf1=0
sf2=0
sf3=0
sf4=0
sf5=0
sf6=0
sf7=0
sf8=0
NewAngle1 =0
NewAngle2 =0
NewAngle3 =0
NewAngle4 =0
NewAngle5 =0
NewAngle6 =0
NewAngle7 =0
NewAngle8 =0
#TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT


#########################################################################################################################################################################################
def repeat4function():	
	global Bi
	global Ri
	global i
	if String[BracketList[Bi+2]] == "<" and String[BracketList[Bi+5]] == ">":
		for i in range(0, RepeatCountList[Ri]):
			tempi = i
			tempBi = Bi
			tempRi = Ri
			basicrepeat(1, BracketList[Bi]+1 ,BracketList[Bi+1]-3)
			Ri=Ri+1
			Bi=Bi+1
			i=BracketList[Bi+1]
			repeat3functionfor4()
			basicrepeat(1, BracketList[Bi]+1 ,BracketList[Bi+1])
			i = tempi
			Bi = tempBi
			Ri = tempRi
		i=BracketList[Bi+7]
		Bi=Bi+8
		Ri=Ri+4
	elif String[BracketList[Bi+2]] == ">" and String[BracketList[Bi+5]] == ">":		
		for i in range(0, RepeatCountList[Ri]):
			tempi = i
			tempBi = Bi
			tempRi = Ri
			Ri=Ri+1
			basicrepeat(1, BracketList[Bi]+1 ,BracketList[Bi+1]-3)
			Bi=Bi+1
			i=BracketList[Bi+1]
			basicrepeat( RepeatCountList[Ri],BracketList[Bi]+1, BracketList[Bi+1])
			Ri=Ri+1
			Bi=Bi+1
			i=BracketList[Bi+1]
			
			basicrepeat(1, BracketList[Bi]+1 ,BracketList[Bi+1]-3)
			Bi=Bi+1
			i=BracketList[Bi+1]
			repeat2functionfor2()
			Bi=Bi-1
			#print Bi
			#print Ri
			basicrepeat(1, BracketList[Bi]+1 ,BracketList[Bi+1])
			i = tempi
			Bi = tempBi
			Ri = tempRi
		i=BracketList[Bi+7]
		Bi=Bi+8
		Ri=Ri+4
	elif String[BracketList[Bi+2]] == "<" and String[BracketList[Bi+5]] == "<":
		for i in range(0, RepeatCountList[Ri]):
			tempi = i
			tempBi = Bi
			tempRi = Ri
			Ri=Ri+1
			basicrepeat(1, BracketList[Bi]+1 ,BracketList[Bi+1]-3)
			Bi=Bi+1
			i=BracketList[Bi+1]
			repeat2functionfor2()
			Bi=Bi-1
			basicrepeat(1, BracketList[Bi]+1 ,BracketList[Bi+1]-3)
			Bi=Bi+1
			basicrepeat(RepeatCountList[Ri], BracketList[Bi]+1 ,BracketList[Bi+1])
			Ri=Ri+1
			Bi=Bi+1
			basicrepeat(1, BracketList[Bi]+1 ,BracketList[Bi+1])
			i = tempi
			Bi = tempBi
			Ri = tempRi
		i=BracketList[Bi+7]
		Bi=Bi+8
		Ri=Ri+4
	elif String[BracketList[Bi+2]] == ">" and String[BracketList[Bi+5]] == "<":
		for i in range(0, RepeatCountList[Ri]):
			tempi = i
			tempBi = Bi
			tempRi = Ri
			Ri=Ri+1
			basicrepeat(1, BracketList[Bi]+1 ,BracketList[Bi+1]-3)
			Bi=Bi+1
			i=BracketList[Bi+1]
			basicrepeat(RepeatCountList[Ri], BracketList[Bi]+1 ,BracketList[Bi+1])
			Ri=Ri+1
			Bi=Bi+1
			basicrepeat(1, BracketList[Bi]+1 ,BracketList[Bi+1]-3)
			Bi=Bi+1
			basicrepeat(RepeatCountList[Ri], BracketList[Bi]+1 ,BracketList[Bi+1])
			Ri=Ri+1
			Bi=Bi+1
			basicrepeat(1, BracketList[Bi]+1 ,BracketList[Bi+1]-3)
			Bi=Bi+1
			basicrepeat(RepeatCountList[Ri], BracketList[Bi]+1 ,BracketList[Bi+1])
			Ri=Ri+1
			Bi=Bi+1
			basicrepeat(1, BracketList[Bi]+1 ,BracketList[Bi+1])
			i = tempi
			Bi = tempBi
			Ri = tempRi
		i=BracketList[Bi+7]
		Bi=Bi+8
		Ri=Ri+4		
#######################################################################################################################################################
def stringdataextractor(String):
	if String != "Y":
		for k in range(0, len(String)):
			if String[k] == "<" or String[k] == ">":
				BracketList.append(k)
				if String[k] == "<":
					RepeatCountList.append(int(String[k-2:k]))
	else :
		print  "in pause"

def basicrepeat(NoOfTimes, Start, End):
	global i
	i=Start
	for j in range(0, NoOfTimes):
		stringiterator_for_repeat(End)
		i = Start
	

def repeat2functionfor3():
	global Bi
	global Ri
	global i
	for k in range(0,RepeatCountList[Ri]):
		basicrepeat(1,BracketList[Bi]+1 ,BracketList[Bi+1]-3)
		basicrepeat(RepeatCountList[Ri+1],BracketList[Bi+1]+1 ,BracketList[Bi+2])
		basicrepeat(1,BracketList[Bi+2]+1 ,BracketList[Bi+3])
	i=BracketList[Bi+3]
	Bi=Bi+3
	Ri=Ri+1

def repeat2functionfor2():
	global Bi
	global Ri
	global i
	for k in range(0,RepeatCountList[Ri]):
		basicrepeat(1,BracketList[Bi]+1 ,BracketList[Bi+1]-3)
		basicrepeat(RepeatCountList[Ri+1],BracketList[Bi+1]+1 ,BracketList[Bi+2])
		basicrepeat(1,BracketList[Bi+2]+1 ,BracketList[Bi+3])
	i=BracketList[Bi+3]
	Bi=Bi+4
	Ri=Ri+2

def repeat3function():	
	global Bi
	global Ri
	global i
	if String[BracketList[Bi+2]] == "<":
		for j in range(0,RepeatCountList[Ri]):
			tempi = i
			tempBi = Bi
			tempRi = Ri
			basicrepeat(1,BracketList[Bi]+1 ,BracketList[Bi+1]-3)
			Ri=Ri+1
			Bi=Bi+1
			i=BracketList[Bi+1]
			repeat2functionfor3()
			basicrepeat(1,BracketList[Bi]+1 ,BracketList[Bi+1])
			i = tempi
			Bi = tempBi
			Ri = tempRi
	
		i=BracketList[Bi+5]
		Bi=Bi+6
		Ri=Ri+3 
		
	elif String[BracketList[Bi+2]] == ">":
		#print "#################################################"
		for j in range(0, RepeatCountList[Ri]):
			tempi = i
			tempBi = Bi
			tempRi = Ri
			basicrepeat(1,BracketList[Bi]+1 ,BracketList[Bi+1]-3)
			basicrepeat(RepeatCountList[Ri+1],BracketList[Bi+1]+1 ,BracketList[Bi+2])
			basicrepeat(1,BracketList[Bi+2]+1 ,BracketList[Bi+3]-3)
			basicrepeat(RepeatCountList[Ri+2],BracketList[Bi+3]+1 ,BracketList[Bi+4])
			basicrepeat(1,BracketList[Bi+4]+1 ,BracketList[Bi+5])
			i = tempi
			Bi = tempBi
			Ri = tempRi
		i=BracketList[Bi+5]
		Bi=Bi+6
		Ri=Ri+3
def repeat3functionfor4():	
	global Bi
	global Ri
	global i
	if String[BracketList[Bi+2]] == "<":
		#print "#######################"+String[BracketList[Bi+2]]
		for j in range(0,RepeatCountList[Ri]):
			tempi = i
			tempBi = Bi
			tempRi = Ri
			basicrepeat(1,BracketList[Bi]+1 ,BracketList[Bi+1]-3)
			Ri=Ri+1
			Bi=Bi+1
			i=BracketList[Bi+1]
			repeat2functionfor3()
			basicrepeat(1,BracketList[Bi]+1 ,BracketList[Bi+1])
			i = tempi
			Bi = tempBi
			Ri = tempRi
	
		i=BracketList[Bi+5]
		Bi=Bi+5
		Ri=Ri+3 
			
	elif String[BracketList[Bi+2]] == ">":
		#print "#################################################"
		for j in range(0, RepeatCountList[Ri]):
			tempi = i
			tempBi = Bi
			tempRi = Ri
			basicrepeat(1,BracketList[Bi]+1 ,BracketList[Bi+1]-3)
			basicrepeat(RepeatCountList[Ri+1],BracketList[Bi+1]+1 ,BracketList[Bi+2])
			basicrepeat(1,BracketList[Bi+2]+1 ,BracketList[Bi+3]-3)
			basicrepeat(RepeatCountList[Ri+2],BracketList[Bi+3]+1 ,BracketList[Bi+4])
			basicrepeat(1,BracketList[Bi+4]+1 ,BracketList[Bi+5])
			i = tempi
			Bi = tempBi
			Ri = tempRi
		i=BracketList[Bi+5]
		Bi=Bi+6
		Ri=Ri+3
	





def loopdecider():
	global Bi
	global Ri
	global i

	if String[i-1] == "4":
		repeat4function()
		
	if String[i-1] == "3":
		repeat3function()
		
	if String[i-1] == "1":
		basicrepeat(RepeatCountList[Ri],BracketList[Bi]+1 ,BracketList[Bi+1])
		i=BracketList[Bi+1]
		Bi=Bi+2
		Ri=Ri+1

	if String[i-1] == "2":
		repeat2functionfor2()

def finalstringprocessor(String):
	global Bi
	global Ri
	global i 
	Bi= 0
	Ri = 0
	i = 0	
	while i<len(String):
		#print "**"+String[i]+"**"
		if String[i] == "R":
			loopdecider()
		i=i+1					

#****************************************************************************************************************************************************************************
def ping():
	time.sleep(0.005)
	global i
	print "ping"
	SenNo = int(String[i+1])
	i = i+2
	#print SenNo
	
	data = ""
	temp = ""
	if SenNo == 0:
		FTs = "FV012"
	elif SenNo == 1:
		FTs = "FV102"
	elif SenNo == 2:
		FTs = "FV201"
	elif SenNo == 3:
		FTs = "FV301"
	por.write(FTs)
	while data != "#":
		data = por.read(1)
		if data == "\n" or data == "\r":
			data = ""
		temp= temp+data
	print temp
	print temp[1:4]
	tpfile = open("t_p.txt","w")
	tpfile.write("p\n")
	tpfile.close()
	pf = open("ping.txt","w")
	pf.write(temp[1:4])	
	pf.close()
	

def calibrate():
	time.sleep(0.005)
	global i
	print "calibrate"
	SenNo = int(String[i+1])
	i = i+2
	#print SenNo
	
	data = ""
	temp = ""
	if SenNo == 0:
		FTs = "FV012"
	elif SenNo == 1:
		FTs = "FV102"
	elif SenNo == 2:
		FTs = "FV201"
	elif SenNo == 5:
		FTs = "FV301"
	while True:
		por.write(FTs)
		while data != "#":
			data = por.read(1)
			if data == "\n" or data == "\r":
				data = ""
			temp= temp+data
		print temp
		print temp[1:4]
		tpfile = open("t_p.txt","w")
		tpfile.write("p\n")
		tpfile.close()
		pf = open("ping.txt","w")
		pf.write(temp[1:4])	
		pf.close()
		time.sleep(.4)
def led():
	time.sleep(0.005)	
	global String
	global i
	print "led"*1000
	por.write(String[i:i+13])
	i=i+13


def map():
	global String
	global i
	print "in map"
	port = String[i+2]
	print ">>>>>"
	print port
	print ">>>>>"
	try:
		print "t"
		omn =int (String[i+3:i+6])
		omx = int(String[i+7:i+11])
		servono = int(String[i+13])-1
		smn =int(String[i+14:i+17])
		smx =int (String[i+18:i+21])
	except:
		print "e"
		omn =int (String[i+3:i+6])
		omx =int ( String[i+7:i+10])
		servono = int(String[i+12])-1
		smn =int (String[i+13:i+16])
		smx = int(String[i+17:i+20])
	if port == "0":
		FT = "FV012."
	elif port == "1":
		FT = "FV120."
	elif port == "2":
		FT = "FV210."
	print omn
	print omx
	print servono
	print smn
	print smx
	amn = smn+50
	amx = smx+50
	OldAngle = 0
	delay = 0.004
	"""
	por.write(FT)
	data = ""
        temp = ""
	while data != "#":
                data = por.read(1)
               	if data == "\n" or data == "\r" :
                	data =""
			temp =temp+data
        string = temp
	"""
	krv = "Y"+port
	#por.write(krv)
        por.write("Y0")
	while True:
	        data = ""
        	temp = ""
	        while data != "#":
        	        data = por.read(1)
                	if data == "\n" or data == "\r" :
                      		data =""
	                temp =temp+data
        	string = temp
		print string
		map=int(string[1:4])
		if map <= omn:
			map = omn
		elif map >= omx:
			map = omx
		NewAngle =int((float(map-omn)/(omx-omn)) *float(smx -smn)+smn)
		b =int( (float(NewAngle-smn)/(smx-smn)) *float(amx -amn)+amn)
                os.system("echo "+str(servono)+"="+str(b)+" > /dev/servoblaster")
		#####################################################33##
	
def buzzer():
	time.sleep(0.005)
	global i
	por.write(String[i:i+4])
	i=i+4

def touch():
	global i
	por.write(String[i:i+3])
	i=i+3
	por.write("Q")
	while True:
		data = ""
		temp = ""
		while data != "#":
			data = por.read(1)
			if data == "\n" :
				data = ""
			temp= temp+data
		touchdata = temp	
		#print touchdata+">>"
		tpfile = open("t_p.txt","w")
		tpfile.write("t\n")
		tpfile.close()
		file =open("touch.txt","w")
		file.write(touchdata)
		file.close()
		

def delay():
	#print "delay"
	global i
	if String[i+5] == "m":
		time.sleep(int(String[i+1:i+5])/1000.0)
		i=i+7
	elif String[i+5] == "s":
		time.sleep(int(String[i+1:i+5]))
		i=i+7
#******************************************************************************************************************************
#******************************************************************************************************************************			
def sensor():
	global i
	global NoOfSensors 
	global SensorPort 
	global ComparingValue
	global LogicalOpr 
	global SensorString 
	global TruePart 
	global FalsePart 
	global TStart 
	global TEnd 
	global FStart 
	global FEnd
	global por
	
	if String.count("{") == 1:
		NoOfSensors =String[i+1:i+2]
		SensorPort =String[i+2:i+3]  
		ComparingValue = int(String[i+4:i+7])
		LogicalOpr = String[i+3:i+4] 
		SensorString =  re.findall("F.*}",String)[0]
		TruePart = re.findall("{.*\|",String)[0][1:-1]
		FalsePart = re.findall("\|.*}",String)[0][1:-1]
		TStart = String.index("{") + 1
		TEnd = String.index("|") - 1 
		FStart = String.index("|") + 1 
		FEnd = String.index("}") - 1
		i=i+len(SensorString)

		#print "olaaaa"	
		#print NoOfSensors
		#print SensorPort
		#print ComparingValue
		#print LogicalOpr
		#print SensorString	
		#print TruePart
		#print FalsePart	
	string = ""
	data = "0"
	
	#usbport1='/dev/ttyAMA0'
	#por1 = serial.Serial(usbport1,9600,timeout=15.0)
	por.flushInput()
	#print "senosreeeeeeeeee"
	file = open('workfile.txt', 'a')
	
	class serial_read_file_write(threading.Thread):
	        def __init__(self):
        	        threading.Thread.__init__(self)
	        def run(self):
			global string
			por.flushInput()
				#print "$"+temp+"***"

	class read_file(threading.Thread):                                                                                          
       		def __init__(self):
       	         	threading.Thread.__init__(self)
        	def run(self):
			global string
                	f1 = open('workfile.txt','r')
                	final = open('final.txt','a')
                	while True:
				#print "("+ f1.readline().strip()+")"
				string =  f1.readline().strip()
				#print string+">"
				if len(string)<1:
					print "nodata"
					string = "00011"
				time.sleep(0.2)
	
	class sensor_function(threading.Thread):
		def __init__(self):
       	         	threading.Thread.__init__(self)
		def run(self):
			global i
			global string
			global NoOfSensors 
			global SensorPort 
			global ComparingValue
			global LogicalOpr 
			global SensorString 
			global TruePart 
			global FalsePart 
			global TStart 
			global TEnd 
			global FStart 
			global FEnd
			#print String[TStart]
			#print String[TEnd]
			#print String[FStart]
			#print String[FEnd]
			if SensorPort == "0":
				FT = "FV012."
			elif SensorPort == "1":
				FT = "FV120"
			elif SensorPort == "2":
				FT = "FV210"
			elif SensorPort == "3":
				FT = "FV310"
			data = ""
			temp = ""
			
			por.write(FT)
			while data != "#":
				data = por.read(1)
				if data == "\n" or data == "\r":
					data =""
					temp =temp+data
			string = temp
			
			if LogicalOpr == "g":
				while True:
					data = ""
					temp = ""
					por.write(FT)
					while data != "#":
						data = por.read(1)
						if data == "\n" or data == "\r":
							data =""
						temp =temp+data
						
					string = temp
					#print "<"+string[1:4]+">"
					SensorValue=int(string[1:4])
					print SensorValue
					if SensorValue > ComparingValue:
						i = TStart
						end = TEnd
						stringiterator_for_sensor(end)
						time.sleep(0.15)
						i = TStart
					else:
						i = FStart
						end = FEnd
						stringiterator_for_sensor(end)
						time.sleep(0.15)
						i = FStart
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
			if LogicalOpr == "l":
				SensorValue = 0
				while True:
					por.write(FT)
					data = ""
					temp = ""
					while data != "#":
						data = por.read(1)
						if data == "\n" or data == "\r":
							data =""
						temp =temp+data
					string = temp
					SensorValue=int(string[1:4])
					print SensorValue
					if SensorValue < ComparingValue:
						i = TStart
						end = TEnd
						stringiterator_for_sensor(end)
						time.sleep(0.15)
						i = TStart
					else:
						i = FStart
						end = FEnd
						stringiterator_for_sensor(end)
						time.sleep(0.15)
						i = FStart
			if LogicalOpr == "e":
				while True:
					por.write(FT)
					data = ""
					temp = ""
					while data != "#":
						data = por.read(1)
						if data == "\n" or data == "\r":
							data =""
						temp =temp+data
					string = temp
					SensorValue=int(string[1:4])
					print SensorValue
					if SensorValue == ComparingValue:
						i = TStart
						end = TEnd
						stringiterator_for_sensor(end)
						time.sleep(0.15)
						i = TStart
					else:
						i = FStart
						end = FEnd
						stringiterator_for_sensor(end)
						time.sleep(0.15)
						i = FStart

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	class sensor_function_for_simultaneous(threading.Thread):
		def __init__(self):
			threading.Thread.__init__(self)
		def run(self):	
			global i
			global string
			global NoOfSensors
			global SensorPort
			global ComparingValue
			global LogicalOpr
			global SensorString
			temp = String
			
			b = 0
			blist=[]
			while temp[b]!=".":
				if temp[b] == "[" or temp[b] == "]" or temp[b] == "|":
					blist.append(b)
					b=b+1
				else:
					b=b+1
			T1s=blist[0]+1
			T1e=blist[1]-1
			F1s=blist[1]+1
			F1e=blist[2]-1
			T2s=blist[3]+1
			T2e=blist[4]-1
			F2s=blist[4]+1
			F2e=blist[5]-1
			#print temp
			Sensordata = re.findall("#F.\d*.",temp)
			FirstSensordata = Sensordata[0]
			SecondSensordata = Sensordata[1]
			#print FirstSensordata
			#print SecondSensordata
			FSN = FirstSensordata[3]
			FV = FirstSensordata[4:7]
			FO = FirstSensordata[-1]
			#print FSN,FV,FO
			SSN =SecondSensordata[3]
			SV = SecondSensordata[4:7]
			SO = SecondSensordata[-1]
			#print SSN,SV,SO
			SensorValue = 0
			if FSN == "0":
				FT = "FV012"
			elif FSN == "1":
				FT = "FV102"
			elif FSN == "2":
				FT= "FV201"
			if SSN == "0":
				ST = "FV012"
			elif SSN == "1":
				ST = "FV102"
			elif SSN == "2":
				ST= "FV201"
			
			while True:
						
                                por.write(FT)
                                data = ""
                                temp = ""
                                while data != "#":
                                	data = por.read(1)
					if data == "\n" or data == "\r":
						data =""
                                        temp =temp+data
                                string1= temp
				print string1[1:4]+ ">"
					
                                SensorValue = int(string1[1:4])
					
				if FO == "g" and SensorValue > int(FV):
					i = T1s
                                        end = T1e
                                        stringiterator_for_sensor(end)
                                        time.sleep(0.3)
                                        i = T1s
                                elif FO == "g":
                                        i = F1s
                                        end = F1e
                                        stringiterator_for_sensor(end)
                                        time.sleep(0.3)
                                        i = F1s
					
				if FO == "l" and SensorValue < int(FV):
                                        i = T1s
                                        end = T1e
                                        stringiterator_for_sensor(end)
                                        time.sleep(0.3)
                                        i = T1s
                                elif FO == "l":
                                        i = F1s
                                        end = F1e
                                        stringiterator_for_sensor(end)
                                        time.sleep(0.3)
                                        i = F1s
				if FO == "e" and SensorValue == int(FV):
                                        i = T1s
                                        end = T1e
                                        stringiterator_for_sensor(end)
                                        time.sleep(0.3)
                                        i = T1s
                                elif FO == "e":
                                        i = F1s
                                        end = F1e
                                        stringiterator_for_sensor(end)
                                        time.sleep(0.3)
                                        i = F1s

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
		
	
	threads = []
	thread = serial_read_file_write()
	thread.start()
	threads.append(thread)
	#thread = read_file()
	#thread.start()
	#threads.append(thread)
	if String.count("{") == 1:
		thread = sensor_function()
	elif String.count("{") == 2:
		thread = sensor_function_for_simultaneous()
	thread.start()
	threads.append(thread)
	for thread in threads:
        	thread.join()
	
	

#$$$$$$$$$$$$$$$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#************************************************ servo motor updated on 23rd nov 2015 **********************************************************************
def servo():
        global i
        #print "servo"
        #print String[i:i+8]
        MotorNo = int(String[i+1:i+2])
        NewAngle = int(String[i+3:i+6])
        Speed = int(String[i+7:i+8])
        #print NewAngle
        #print MotorNo
        #print Speed
        #por.write(String[i:i+8])
        i=i+8
        insideservo(MotorNo, NewAngle, Speed)

def insideservo(ServoNo, NewAngle, Speed):
        print NewAngle
        global S1OldAngle
        global S2OldAngle
        global S3OldAngle
        global S4OldAngle
        global S5OldAngle
        global S6OldAngle
        global S7OldAngle
        global S8OldAngle
        delay = (10-Speed)*0.004
        b= 50
        if ServoNo == 1:
                if Speed == 1:
                        os.system("echo 0="+str(NewAngle+50)+" > /dev/servoblaster")
                        S1OldAngle = NewAngle
                elif  NewAngle+50 > S1OldAngle+50:
                        #print str(S1OldAngle)+"old aangle >>"
                        b=S1OldAngle+50
                        while b < NewAngle+1+50 and b<231:
                                os.system("echo 0="+str(b)+" > /dev/servoblaster")
                                b=b+1
                                time.sleep(delay)
                                #print b
                        S1OldAngle = NewAngle
                elif  NewAngle+50 < S1OldAngle+50:
                        b=S1OldAngle+50
                        while b>51 and b > NewAngle+50-1:
                                b=b-1
                                os.system("echo 0="+str(b)+" > /dev/servoblaster")
                                time.sleep(delay)
                                #print b
                        S1OldAngle = NewAngle
                else :
                        pass

	elif ServoNo == 2:
                if Speed == 1:
                        os.system("echo 1="+str(NewAngle+50)+" > /dev/servoblaster")
                        S1OldAngle = NewAngle
                elif  NewAngle+50 > S2OldAngle+50:
                        #print str(S2OldAngle)+"old aangle >>"
                        b=S2OldAngle+50
                        while b < NewAngle+1+50 and b<231:
                                os.system("echo 1="+str(b)+" > /dev/servoblaster")
                                b=b+1
                                time.sleep(delay)

                        S2OldAngle = NewAngle
                elif  NewAngle+50 < S2OldAngle+50:
                        b=S2OldAngle+50
                        while b>51 and b > NewAngle+50-1:
                                b=b-1
                                os.system("echo 1="+str(b)+" > /dev/servoblaster")
                                time.sleep(delay)
                                #print b
                        S2OldAngle = NewAngle
                else :
                        pass



	elif ServoNo == 3:
                if Speed == 1:
                        os.system("echo 2="+str(NewAngle+50)+" > /dev/servoblaster")
                        S1OldAngle = NewAngle
                elif  NewAngle+50 > S3OldAngle+50:
                        #print str(S3OldAngle)+"old aangle >>"
                        b=S3OldAngle+50
                        while b < NewAngle+1+50 and b<231:
                                os.system("echo 2="+str(b)+" > /dev/servoblaster")
                                b=b+1
                                time.sleep(delay)
                                #print b
                        S3OldAngle = NewAngle
                elif  NewAngle+50 < S3OldAngle+50:
                        b=S3OldAngle+50
                        while b>51 and b > NewAngle+50-1:
                                b=b-1
                                os.system("echo 2="+str(b)+" > /dev/servoblaster")
                                time.sleep(delay)
                                #print b
                        S3OldAngle = NewAngle
                else :
                        pass

        elif ServoNo == 4:
                if Speed == 1:
                        os.system("echo 3="+str(NewAngle+50)+" > /dev/servoblaster")
                        S1OldAngle = NewAngle
                elif  NewAngle+50 > S4OldAngle+50:
                        print str(S4OldAngle)+"old aangle >>"
                        b=S4OldAngle+50
                        while b < NewAngle+1+50 and b<231:
                                os.system("echo 3="+str(b)+" > /dev/servoblaster")
                                b=b+1
                                time.sleep(delay)
                                #print b
                        S4OldAngle = NewAngle
                elif  NewAngle+50 < S4OldAngle+50:
                        b=S4OldAngle+50
                        while b>51 and b > NewAngle+50-1:
                                b=b-1
                                os.system("echo 3="+str(b)+" > /dev/servoblaster")
                                time.sleep(delay)
                                #print b
                        S4OldAngle = NewAngle
                else :
                        pass




	elif ServoNo == 5:
                if Speed == 1:
                        os.system("echo 4="+str(NewAngle+50)+" > /dev/servoblaster")
                        S1OldAngle = NewAngle
                elif  NewAngle+50 > S5OldAngle+50:
                        #print str(S5OldAngle)+"old aangle >>"
                        b=S5OldAngle+50
                        while b < NewAngle+1+50 and b<231:
                                os.system("echo 4="+str(b)+" > /dev/servoblaster")
                                b=b+1
                                time.sleep(delay)
                                #print b
                        S5OldAngle = NewAngle
                elif  NewAngle+50 < S5OldAngle+50:
                        b=S5OldAngle+50
                        while b>51 and b > NewAngle+50-1:
                                b=b-1
                                os.system("echo 4="+str(b)+" > /dev/servoblaster")
                                time.sleep(delay)
                                #print b
                        S5OldAngle = NewAngle
                else :
                        pass
        elif ServoNo == 6:
                if Speed == 1:
                        os.system("echo 5="+str(NewAngle+50)+" > /dev/servoblaster")
                        S1OldAngle = NewAngle
                elif  NewAngle+50 > S6OldAngle+50:
                        #print str(S6OldAngle)+"old aangle >>"
                        b=S6OldAngle+50
                        while b < NewAngle+1+50 and b<231:
                                os.system("echo 5="+str(b)+" > /dev/servoblaster")
                                b=b+1
                                time.sleep(delay)
                                #print b
                        S6OldAngle = NewAngle
                elif  NewAngle+50 < S6OldAngle+50:
                        b=S6OldAngle+50
                        while b>51 and b > NewAngle+50-1:
                                b=b-1
                                os.system("echo 5="+str(b)+" > /dev/servoblaster")
                                time.sleep(delay)
                                #print b
                        S6OldAngle = NewAngle
                else :
                        pass


        elif ServoNo == 7:
                if Speed == 1:
                        os.system("echo 6="+str(NewAngle+50)+" > /dev/servoblaster")
                        S1OldAngle = NewAngle
                elif  NewAngle+50 > S7OldAngle+50:
                        #print str(S7OldAngle)+"old aangle >>"
                        b=S7OldAngle+50
                        while b < NewAngle+1+50 and b<231:
                                os.system("echo ="+str(b)+" > /dev/servoblaster")
                                b=b+1
                                time.sleep(delay)
                                #print b
                        S6OldAngle = NewAngle
                elif  NewAngle+50 < S7OldAngle+50:
                        b=S7OldAngle+50
                        while b>51 and b > NewAngle+50-1:
                                b=b-1
                                os.system("echo 6="+str(b)+" > /dev/servoblaster")
                                time.sleep(delay)
                                #print b
                        S7OldAngle = NewAngle
                else :
                        pass
        elif ServoNo == 8:
                if Speed == 1:
                        os.system("echo 7="+str(NewAngle+50)+" > /dev/servoblaster")
                        S1OldAngle = NewAngle
                elif  NewAngle+50 > S8OldAngle+50:
                        #print str(S8OldAngle)+"old aangle >>"
                        b=S8OldAngle+50
                        while b < NewAngle+1+50 and b<231:
                                os.system("echo 0="+str(b)+" > /dev/servoblaster")
                                b=b+1
                                time.sleep(delay)
                                #print b
                        S8OldAngle = NewAngle
                elif  NewAngle+50 < S1OldAngle+50:
                        b=S8OldAngle+50
                        while b>51 and b > NewAngle+50-1:
                                b=b-1
                                os.system("echo 0="+str(b)+" > /dev/servoblaster")
                                time.sleep(delay)
                                #print b
                        S8OldAngle = NewAngle
                else :
                        pass


#*************************************************************************************************************************************

def lcd():
	print "lcd"
	time.sleep(.005)
	global i
	por.write(String[i:i+38])	
	i=i+38
def stringiterator_for_repeat(end):
	global i			
	while i<end:
		if String[i] == "W":
			
			led()				
		elif String[i] == "Z":
			#print "BUZZERf"
			buzzer()	
		elif String[i] == "C":
			print "calibrate"
			calibrate()	
		elif String[i] == "L":
			#print "LCD"
			lcd()
		elif String[i] == "Q":
			#print "Touchf"
			touch()
		elif String[i] == "T":
			delay()
		elif String[i] == "F":
			#print "Sensorf"
			sensor()
		elif String[i] == "M":
			#print "Motorf" 
			motor()
		elif String[i] == "S":
			#print "servof"
			servo()	
		elif String[i] == "P":
			print "ping"
			ping()	
		elif String[i] == "#":
			i=i+1
		else:
			i = i+1

def stringiterator_for_sensor(end):
	global i			
	while i<end:
		if String[i] == "W":
			
			led()				
		elif String[i] == "Z":
			#print "BUZZERf"
			buzzer()	
		elif String[i] == "C":
			print "calibrate"
			calibrate()	
		elif String[i] == "L":
			#print "LCD"
			lcd()
		elif String[i] == "Q":
			#print "Touchf"
			touch()
		elif String[i] == "T":
			delay()
		elif String[i] == "M":
			#print "Motor" 
			motor()
		elif String[i] == "S":
			#print "servo"
			servo()	
		elif String[i] == "R":
			loopdecider()
		else:
			i=i+1
		
		

def motor():
	global i
	time.sleep(0.005)
	print String[i+1]
	if int(String[i+1]) <=2:
		por.write(String[i:i+4])
		i=i+4
	else :
		pass	
	
	





def main_stringiterator():
	global Bi
	global Ri
	global i 
	Bi= 0
	Ri = 0
	i = 0			
	if String[i]=="Y":
		return 0
	slen = len(String)
	while i<slen:
	#while String[i]!=".":
		if String[i] == "P":
			ping()
		elif String[i] == "W":
			led()				
		elif String[i] == "Z":
			#print "BUZZERf"
			buzzer()	
		elif String[i] == "L":
			#print "LCD"
			lcd()
		elif String[i] == "C":
			print "calibrate"
			calibrate()	
		elif String[i] == "Q":
			#print "Touchf"
			touch()
		elif String[i] == "T":
			delay()
		elif String[i] == "F":
			sensor()
		elif String[i] == "M":
			#print "Motor" 
			motor()
		elif String[i] == "S":
			#print "servo"
			servo()	
		elif String[i] == "R":
			loopdecider()
		elif String[i] == "Y":
			map()
			
		else:
			i=i+1
	
#****************************************************************************************************************************************************************************					

def normaloperation():
	print "in normal operation"
	global nflag
	global String
	global iotdata
	while True:
		if nflag == 1:
			
	 		String = iotdata.strip()
		        stringdataextractor(String)
        		por.write("N")
		        time.sleep(1)
			lenr = len(RepeatCountList)
			for c in range(0,lenr):
				if RepeatCountList[c] == 0:
					RepeatCountList[c] = 65535
        		le=open("check","w")
        		main_stringiterator()
			nflag = 0
		elif nflag == 0:
			pass
		time.sleep(.1)
def main():
	print "in iot main thread"
 	global BracketList 
        global RepeatCountList 
        global Bi
	global Ri 
	global i 
	global iotdata
	global nflag
	global String
        flagfile=open("iotflag.txt","w")
        flagfile.write(str(1)+"\n")
        flagfile.close()
        our_thread=threading.Thread(target =readfromcloud)
        our_thread.setDaemon(True)
        our_thread.start()
        our_thread=threading.Thread(target =normaloperation)
        our_thread.setDaemon(True)
        our_thread.start()
	
	while 1:
		#print "N flag value = "+str(nflag)
                flagfile=open("iotflag.txt","r")
                flag = flagfile.readline()
                flagfile.close()
                if flag.strip() == "1":
                        flagfile=open("iotflag.txt","w")
                        flagfile.write(str(0)+"\n")
                        flagfile.close()
                        file= open("iotdata.txt","r")
                        iotdata =file.readline()
                        file.close()
			if iotdata.strip() == "#W000,000,000,.":
				file=open("wifi_mode.txt","w")
                                file.write("a")
                                file.close()
				i=open("iotdata.txt","w")
				i.write("Y.")
				i.close()
                                os.chdir("/etc/network")
                                os.system("rm interfaces")
                                os.system("cp interfaces.apnmode interfaces")
                                os.system("sudo reboot")
			nflag = 1
		else:
			pass
			#nflag = 0
main()
