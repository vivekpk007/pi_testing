import threading
import time
import sys
import socket
import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

WiFi_mode = 7
WiFi_status = 8
WiFi_switch = 25

GPIO.setup(WiFi_mode,GPIO.OUT)
GPIO.setup(WiFi_switch,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(WiFi_status,GPIO.OUT)


def switch():
	while True:
       		if GPIO.input(WiFi_switch) == 0:
			if mode == "s":
				file=open("wifi_mode.txt","w")
		                file.write("a")
                		file.close()
		                os.chdir("/etc/network")
                		os.system("rm interfaces")
		                os.system("cp interfaces.apnmode interfaces")
                		os.system("sudo reboot")
			elif mode == "a":
				file=open("wifi_mode.txt","w")
		                file.write("s")
                		file.close()
		                os.chdir("/etc/network")
	                	os.system("rm interfaces")
	        	        os.system("cp interfaces.stamode interfaces")
                		os.system("sudo reboot")


def b():
	global wifi_ok
        global c
        while True:
		try:
	                print "please connect to the network"
        	        c, addr = s.accept()
	                #print addr
        	        y=c.recv(1024)
                	number = int(y[1:4])
	                #print number
        	        result = ((number%9)+(number%5)+7)*31
                	c.sendall(str(result))
			wifi_ok =1
		except:
			pass


def appdatacollection():
	global wifi_ok
	while wifi_ok == 0:
		pass
	

	while True:
		y=c.recv(1024)
		if y.strip() == "":
			y="Y"
		file= open("appdata.txt","w")
		file.write(y.strip())
		file.close()
		if y.strip() != "." or y.strip() != "Y":
			filels= open("laststring.txt","w")
			filels.write(y.strip())
			filels.close()
		flagfile= open("flag.txt","w")
		flagfile.write(str(1)+"\n")
		flagfile.close()
		if y.startswith("#A"):
			time.sleep(5)
	

def pingtouch():
        while True:
                try:
                        f = open("t_p.txt","r")
                        flag = f.readline()
                        f.close()
                        if flag.strip() == "t":
                                fi = open("touch.txt","r")
                                c.sendall(fi.readline()+"\n")
                                fi.close()
                                f = open("t_p.txt","w")
                                f.write("0")
                                f.close()
                        if flag.strip() == "p":
				#print "wifiping"
                                time.sleep(0.1)
                                fi = open("ping.txt","r")
                                bt= fi.readline()
                                c.sendall(bt.strip())
                                print "ping data sent"
                                fi.close()
                                f = open("t_p.txt","w")
                                f.write("0")
                                f.close()

                        else:
                                pass
                except:
                        pass


def main():
        our_thread=threading.Thread(target =appdatacollection)
        our_thread.setDaemon(True)
        our_thread.start()
        our_thread=threading.Thread(target =b)
        our_thread.setDaemon(True)
        our_thread.start()
        our_thread=threading.Thread(target =switch)
        our_thread.setDaemon(True)
        our_thread.start()
        our_thread=threading.Thread(target =pingtouch)
        our_thread.setDaemon(True)
        our_thread.start()
	while True:
		os.system("sudo python _subcode.py")
		time.sleep(3)
		file= open("appdata.txt","r")
		breakdata = file.readline().strip()
		file.close()
		if breakdata == "#Z9o.":
			c.shutdown(2)
			c.close()
			sys.exit(1)
		elif breakdata == "#W000,000,000,.":
			file=open("wifi_mode.txt","w")
		        file.write("s")
                	file.close()
		        os.chdir("/etc/network")
	              	os.system("rm interfaces")
	                os.system("cp interfaces.stamode interfaces")
                	os.system("sudo reboot")



#**************************************************************** code starts here  *********************************************************************************

file=open("wifi_mode.txt","r")
mode = file.readline().strip()
file.close()

if mode == "s":
        our_thread=threading.Thread(target =switch)
        our_thread.setDaemon(True)
        our_thread.start()
	GPIO.output(WiFi_mode,1)
	
	while True:
		os.system("python _iotcode.py")
else:
	GPIO.output(WiFi_mode,0)









s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

host = "1.2.3.4"
port=8899
wifi_ok = 0
s.bind((host, port))
s.listen(5)

flagfile= open("flag.txt","w")
flagfile.write(str(1)+"\n")
flagfile.close()

main()
