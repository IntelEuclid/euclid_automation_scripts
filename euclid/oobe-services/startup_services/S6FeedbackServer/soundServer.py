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

class SoundPipe:
    def __init__(self):
        self.requests = Queue.Queue()
        Thread(target=self.control).start()

    def AddRequest(self,request):
        self.requests.put(request)

    def control(self):
       
        while True:
            if not self.requests.empty():  
                req = self.requests.get()
                subprocess.call(['gst-launch-1.0 playbin uri=file:///' + req.GetText()],shell=True)
            time.sleep(0.5)


class SoundRequest:
    def __init__(self,req):
        self.request = req[2:len(req)]

    def GetText(self):
        return self.request


class ClientThread(Thread):
    def __init__(self,sound,conn,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
    def run(self):
        data = conn.recv(2048)
        if data[0] == 'P':
            req = SoundRequest(data)
            sound.AddRequest(req)





if __name__ == '__main__':
    sound = SoundPipe()
    TCP_PORT = 8998
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind(('127.0.0.1',TCP_PORT))

    while True:
        tcpServer.listen(4)
        conn,(ip,port) = tcpServer.accept()
        newClient = ClientThread(sound,conn, ip, port)
        newClient.start()


