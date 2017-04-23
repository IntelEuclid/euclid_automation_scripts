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

import sys
import pickle
TCP_IP = '127.0.0.1'
TCP_PORT = 8881
BUFFER_SIZE = 1024

class NetworkFlowFacade(object):

    @staticmethod
    def RequestNetworkRescan():
        """
        Post message call to request system network scan.
        :return : True if call posted, Otherwise False.
        """
        try:           
            import socket
            arr = ["/scan"]
            MESSAGE = pickle.dumps(arr)
            socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.connect((TCP_IP, TCP_PORT))
            socket.send(MESSAGE)
            socket.close()
            return True
        except Exception as e:
            print >>sys.stderr,'Rescan Networks Failed, Error: {}'.format(str(e.message))
            return False
    
    @staticmethod
    def RequestRegisterNetwork(ssid,password):
        """
        Post message call to request to register and connect new network.
        :ssid SSID network name to connect to.
        :password password for the network to connect to.
        :return : True if call posted, Otherwise False.
        """
        try:            
            import socket
            arr = ["/register",ssid,password]
            MESSAGE = pickle.dumps(arr)
            socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.connect((TCP_IP, TCP_PORT))
            socket.send(MESSAGE)
            socket.close()  
            return True  
        except Exception as e:
            print >>sys.stderr,'Register Network Failed, Error: {}'.format(str(e.message))
            return False

    @staticmethod
    def RequestConnectNetwork(ssid):
        """
        Post message call to request to connect to existing network.
        :ssid SSID network name to connect to.
        :return : True if call posted, Otherwise False.
        """
        try:
            import socket          
            arr = ["/connect",ssid]
            MESSAGE = pickle.dumps(arr)
            socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.connect((TCP_IP, TCP_PORT))
            socket.send(MESSAGE)
            socket.close()    
            return True
        except Exception as e:
            print >>sys.stderr,'Connect Network Failed, Error: {}'.format(str(e.message))
            return False
    
    @staticmethod
    def RequestReConnectNetwork():
        """
        Post message call to request to reconnect to existing network.
        :return : True if call posted, Otherwise False.
        """
        try:
            import socket          
            arr = ["/reconnect"]
            MESSAGE = pickle.dumps(arr)
            socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.connect((TCP_IP, TCP_PORT))
            socket.send(MESSAGE)
            socket.close()    
            return True
        except Exception as e:
            print >>sys.stderr,'Reconnect Network Failed, Error: {}'.format(str(e.message))
            return False

    @staticmethod
    def RequestConnectHotspot():
        """
        Post message call to request to load hotspot.
        :return : True if call posted, Otherwise False.
        """
        try:
            import socket            
            arr = ["/start_hotspot"]
            MESSAGE = pickle.dumps(arr)
            socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.connect((TCP_IP, TCP_PORT))
            socket.send(MESSAGE)
            socket.close()   
            return True 
        except Exception as e:
            print >>sys.stderr,'Request Connect Hotspot Failed, Error: {}'.format(str(e.message))
            return False

    @staticmethod
    def GetAvailableNetworkList():
        '''
        Get the saved list of Available networks.
        :return collection of available networks.
        :raise: exception when operation returned errors.
        '''
        try:
            from CsAvailableNetworkList import AvailableNetworkList
            networkList = AvailableNetworkList()
            wifiList = networkList.GetAvailableNetworks()
            return wifiList
        except Exception as e:
            raise e
 
    @staticmethod
    def GetRegisteredNetworks():
        '''
        Get list of registered WiFi networks
        Return: CsGetSavedNetworksResponse(wifiList).  
        '''
        try:
            from EuclidNetworkHAL import EuclidNetworkHAL
            networkHAL = EuclidNetworkHAL()
            wifiList = networkHAL.GetRegisteredNetworks()
            return wifiList
        except Exception as e:
            raise e

    @staticmethod
    def GetCurrentConneectionName():
        '''
         get current Connection name if connected
        :return: Connection name or empty if not connected.
        :raise: exception if operation returned errors.
        '''
        try:
            from EuclidNetworkHAL import EuclidNetworkHAL
            euclidNetworkHAL = EuclidNetworkHAL()
            
            connectionName = euclidNetworkHAL.GetCurrentConnectionName()
            return connectionName
        except Exception as e:
            print >>sys.stderr,'Get Current Connection Name Failed, Error: {}'.format(str(e.message))

    @staticmethod
    def RequestServiceStop():
        '''
         Request Service to stop.
        :return: True if request sent, otherwise false.
        :raise: exception if operation returned errors.
        '''
        try:
            import socket            
            arr = ["/stop_service"]
            MESSAGE = pickle.dumps(arr)
            socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.connect((TCP_IP, TCP_PORT))
            socket.send(MESSAGE)
            socket.close()   
            return True 
        except Exception as e:
            print >>sys.stderr,'Request Stop Network Flow Service Failed, Error: {}'.format(str(e.message))
            return False
