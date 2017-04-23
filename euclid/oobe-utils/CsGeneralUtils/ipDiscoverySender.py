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

import commands
import socket
import struct
import sys
from threading import Thread
import time
import argparse

class DiscoverySender(object):
    def __init__(self, message, local_ip , multicast_ip, multicast_port, interval):
        """ Initialize the Multicast discovery sender ."""

        self._multicast_group = (multicast_ip, multicast_port)
        self._senderThread = None
        self._run = True
        self._message = message
        self._interval = interval
        self._local_IP = local_ip
        self._createSocket()

    def _createSocket(self):
        try:
            # Create the out socket
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.setblocking(1)
            self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 10)
            if self._local_IP is None or self._local_IP == '':
                self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.INADDR_ANY)
            else:
                self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(self._local_IP))
        except socket.error, e:
            print >>sys.stderr, str(e)

    def _sendMessage(self):
        try:
            while(self._run):
                sent = self._sock.sendto(self._message, self._multicast_group)
                time.sleep(self._interval)
        except socket.error, e:
            print >>sys.stderr, str(e)
        except Exception, e:
            print str(e)
        finally:
            self._sock.close()

    def StartSending(self):
        """
        Start the sending message thread to publish message in loop.
        """
        try:
            if (self._senderThread is None):
                self._senderThread = Thread(target = self._sendMessage, args=[])
            if (self._senderThread.is_alive() is False):
                self._senderThread.start()
        except Exception, e:
            print str(e)

    def StopSending(self):
        """
        Signal Sender thread to stop sending messages, and wait for sender.
        Call is blocked, Timeout for waiting is sending interval * 2 (self._interval * 2)
        """
        try:
            self._run = False
            if(self._senderThread is not None):
                self._senderThread.join(self._interval * 2)
        except Exception, e:
            print str(e)

    def __del__(self):
        """
        Destructor to kill thread is not killed
        FIXME: need to check socket.
        """
        if (self._senderThread is not None):
            self._senderThread = None

if __name__ == '__main__':
    # message = 'Hello', local_ip = None , multicast_ip = '224.1.1.100', multicast_port = 10000, interval = 0.5):

    parser = argparse.ArgumentParser(description='IP Discovery Sender.')
    parser.add_argument('--message', default='Hello', help='message to send')
    parser.add_argument('--local_ip',default=None, help='Local IP of the sender')
    parser.add_argument('--multicast_ip',default='224.1.1.100', help='Multicast group address')
    parser.add_argument('--multicast_port',default=10000, type=int, help='Multicast port number')
    parser.add_argument('--interval', default=0.5, type=float, help='Time interval between messages')
    args = parser.parse_args()

    print (args.message)
    print (args.local_ip)
    print (args.multicast_ip)
    print (args.multicast_port)
    print (args.interval)

    sender = DiscoverySender(args.message,args.local_ip,args.multicast_ip,args.multicast_port,args.interval)
    sender.StartSending()
    time.sleep(5000)
    sender.StopSending()
    print('Sender Stopped')