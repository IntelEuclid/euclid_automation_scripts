#!/usr/bin/env python

##################################################################################
#Copyright (c) 2016, Intel Corporation
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this
#list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice,
#this list of conditions and the following disclaimer in the documentation
#and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its contributors
#may be used to endorse or promote products derived from this software without
#specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##################################################################################

import socket
from threading import Thread
from SocketServer import ThreadingMixIn
import Queue
import time
import subprocess
time_milli = lambda: int(round(time.time()*1000))


class GreenLED:
    def __init__(self):
        self.requests = Queue.Queue()
        self.DefaultRequest = LEDRequest('R0$1')
        Thread(target=self.control).start()
    def AddRequest(self,request):
        self.requests.put(request)
    
    def control(self):

        self.currentRequest = ''
        self.state = '1'
        while True:
            if not self.requests.empty():
                request = self.requests.get()
                self.currentRequest = request
            else:
                if self.currentRequest != '' and self.currentRequest.GetRepeat() != 0:
                    request = self.currentRequest
                else:
                    self.currentRequest = ''
                    request = self.DefaultRequest
            
            start_time = time_milli()
            delta = request.getTime()
            pattern = request.GetPattern()
            size = request.GetSize()

            i = 0
            while i < size:
                if pattern[i] == '1' and self.state != '1':

                    subprocess.call(['echo 1 > /sys/class/power_supply/bq24192_charger/led1_control'],shell=True)
                    self.state = '1'
                else:
                    if pattern[i] == '0' and self.state != '0':

                        self.state = '0'
                        subprocess.call(['echo 0 > /sys/class/power_supply/bq24192_charger/led1_control'],shell=True)

                i = i+1
                time.sleep(round(delta)/1000)
            time.sleep(0.5)



class LEDRequest:
    def __init__(self,pattern):
        self.repeat = 1
        self.is_infinite = False
        if pattern[0] == 'R':
            i = 1
            repeat = 0
            while pattern[i] != '$':
                repeat = repeat * 10
                repeat += int(pattern[i])
                i = i +1
            self.repeat = repeat
            if repeat == 0:
                self.is_infinite = True
        self.patternLength = len(pattern)-i-1

        self.pattern = pattern[i+1:len(pattern)]

       

    def getTime(self):
        return 200

    def GetPattern(self):
        return self.pattern

    def GetSize(self):
        return self.patternLength
    
    def GetRepeat(self):
        if self.is_infinite:
            return 1
        self.repeat = self.repeat -1

        return self.repeat +1

class ClientThread(Thread):
    def __init__(self,led,conn,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.led = led
    def run(self):
        data = conn.recv(2048)
        if data[0] == 'R':
            req = LEDRequest(data)
            led.AddRequest(req)
       




if __name__ == '__main__':
    led = GreenLED()
    TCP_PORT = 8999
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind(('127.0.0.1',TCP_PORT))

    while True:
        tcpServer.listen(4)
        conn,(ip,port) = tcpServer.accept()
        newClient = ClientThread(led,conn, ip, port)
        newClient.start()


