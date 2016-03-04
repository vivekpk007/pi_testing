
# IOT CODE **************************************************************************************
import re
import time
import os
import threading
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
    global yureka_str
    file=open(filename,"r")
    data =file.read()
    file.close()
    list = re.findall("iot[\d][\d][\d]",data)
    #rint list
    numlist = []
    for entry in list:
                #rint int(entry[-3:])
                numlist.append(int(entry[-3:]))
    #print numlist
    curmax= max(numlist)
    if curmax < 9 :
	curmax = "00"+str(curmax)
    elif curmax > 9 and curmax <100 :
	curmax = "0"+str(curmax)
    else:
	curmax = str(curmax)	
    print curmax
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
	
	ifile=open("appdata.txt","w")
	ifile.write(matches[0])
	ifile.close()
	ffile=open("flag.txt","w")
	ffile.write("1")
	ffile.close()
        iotsend("iot"+str(curmax)+"ACK")

    else:
        print "fail"

def readfromcloud():
	print "hello"
	while True:
		os.system("curl --header \"carriots.apikey:41d753080c1a2a72515e2fff11d116cdd8f7e91a5b3a2b278b9612af135edc71\" \"http://api.carriots.com/streams/?device=iPhone6Mobile@BOTRIO.BOTRIO\" > hi.txt ")
		readfile("hi.txt")
		time.sleep(3)
def main():
	print "in iot main thread"
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



readfromcloud()
