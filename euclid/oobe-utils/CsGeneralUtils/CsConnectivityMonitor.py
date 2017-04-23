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

import time
from EuclidNetworkHAL import EuclidNetworkHAL
from speechClientFacade import SpeechClientFacade
from CsAvailableNetworkList import AvailableNetworkList
import EuclidConfigHelper
from ipDiscoverySender import DiscoverySender
from threading import Thread
import CsOobeHelper 
from datetime import datetime
from datetime import timedelta
import socket
import sys
import pickle

class CsConnectivityMonitor(object):
   
    def __init__(self):
        try:

            self._safe = False
            self._busy = False
            
            self._run = True
            self._networkHAL = EuclidNetworkHAL()
            print "?"
            currentNetwork = self._networkHAL.GetCurrentConnectionName()
            print "Hal.."
            if currentNetwork == self._networkHAL.LOCAL_HOTSPOT_NAME:
                self._state = 'NORMAL_HS'
            else:
                self._state = 'NORMAL_EXT'
                    
            self._interval = 10
            self._lastDisconnect = None
            self._disconnectTimeout = 30 # in seconds
            self._skipNetworkMonitor = False # Signal system we are in network flow so no fallback needed.
            self._inSafeMode = False

            # Reset available networks list at first boot.
            print "Resetting.."
            self._resetAvailableNetworkList()
            print "done"
            # IP Discovery Server
            self._ipDiscoverySender = None
            print "Starting ip discovery.."
            self._initIPDiscoveryService()

            # Flow Server
            self._tcpIP = '127.0.0.1'
            self._port = 8881
            self._bufferSize = 1024
            self._serverThread = None
            self._sock = None
            print "starting network flow"
            self._startNetworkFlowServer()   
                 
        except Exception, e:
            print >>sys.stderr, 'Init connectivity Network Controller, Error: {}'.format(str(e.message))

    def _resetAvailableNetworkList(self):
        '''
        Reset available network list to empty list.
        '''
        print "Resetting!"
        emptyList = []
        print "Getting avilable.."
        availableNetList = AvailableNetworkList()
        print "Removing"
        availableNetList.SetNetworkList(emptyList)
        print "Done removing"

    def _startNetworkFlowServer(self):
        """
        Start the network requests message thread.
        """
        try:
            if (self._serverThread is None):
                self._serverThread = Thread(target = self._runNetworkFlowServer, args=[])
            if (self._serverThread.is_alive() is False):
                self._serverThread.start()
        except Exception, e:
            print str(e)

    def _runNetworkFlowServer(self):
        try:
            # Create the socket
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.bind((self._tcpIP, self._port))
            self._sock.listen(1)    
            print('Network Flow Service Ready')
            
            #SpeechClientFacade.RequestSay('Network Flow Service Is Ready')            
            while self._run:
                try:
                    conn, addr = self._sock.accept()
                    data = conn.recv(self._bufferSize)
                    if not data: 
                        break

                    data_arr = pickle.loads(data)
                    time.sleep(1) # wait before process message
                    
                    # Suspend connectivity monitor from doing any fallback.
                    self._busy = True

		    SpeechClientFacade.NotifyStart()

                    command = data_arr[0]

                    if "/scan" in command:
                        self.scanNetworks()

                    elif "/register" in command:
                        ssid = data_arr[1]
                        passwd = data_arr[2]
                        currentNetwork = self._networkHAL.GetCurrentConnectionName()
                        # Stopping IP discovery and oobe
                        self.StopIPDiscovery()
                        CsOobeHelper.StopOOBELiveNet()
                        
                        if currentNetwork == self._networkHAL.LOCAL_HOTSPOT_NAME:

                            res = self.connectToNewNetwork(ssid,passwd)
                            newNetwork = ssid
                            if not res:
                                self.connectToNetwork(self._networkHAL.LOCAL_HOTSPOT_NAME,True)
                                newNetwork = self._networkHAL.LOCAL_HOTSPOT_NAME
                            
                        
                        else:
                            res = self.connectToNewNetwork(ssid,passwd)
                            newNetwork = ssid
                            if not res:
                                res = self.connectToNetwork(currentNetwork,False)
                                newNetwork = currentNetwork
                                
                                if not res:
                                    self.connectToNetwork(self._networkHAL.LOCAL_HOTSPOT_NAME,True)
                                    newNetwork = self._networkHAL.LOCAL_HOTSPOT_NAME
                                    
                        # Starting IP discovery and oobe
                        print "Setting network: " + newNetwork
                        EuclidConfigHelper.SetSSIDInConfig(newNetwork)         
                        CsOobeHelper.StartOOBELiveNet()
                        self.RestartIPDiscovery()

                
                    elif "/connect" in command:
                        ssid = data_arr[1]
                        currentNetwork = self._networkHAL.GetCurrentConnectionName()
                        # Stopping IP discovery and oobe
                        self.StopIPDiscovery()
                        CsOobeHelper.StopOOBELiveNet()
                        
                        if currentNetwork == self._networkHAL.LOCAL_HOTSPOT_NAME:

                            res = self.connectToNetwork(ssid,False)
                            newNetwork = ssid
                            if not res:
                                self.connectToNetwork(self._networkHAL.LOCAL_HOTSPOT_NAME,True)
                                newNetwork = self._networkHAL.LOCAL_HOTSPOT_NAME
                            
                        
                        else:
                            res = self.connectToNetwork(ssid)
                            newNetwork = ssid
                            if not res:
                                res = self.connectToNetwork(currentNetwork,False)
                                newNetwork = currentNetwork
                                
                                if not res:
                                    self.connectToNetwork(self._networkHAL.LOCAL_HOTSPOT_NAME,True)
                                    newNetwork = self._networkHAL.LOCAL_HOTSPOT_NAME
                                    
                        # Starting IP discovery and oobe
                        EuclidConfigHelper.SetSSIDInConfig(newNetwork)
                        CsOobeHelper.StartOOBELiveNet()
                        self.RestartIPDiscovery()

                        
                    elif "/reconnect" in command:
                        print "Reconnecting in safe mode.., not reset is required"
                        CsOobeHelper.ExitSafeMode()
                        self._doNetworkFallback()
                        

                    elif "/start_hotspot" in command:
                        currentNetwork = self._networkHAL.GetCurrentConnectionName()
                        if currentNetwork == self._networkHAL.LOCAL_HOTSPOT_NAME:
                            return True
                            
                        self.StopIPDiscovery()
                        CsOobeHelper.StopOOBELiveNet()    
                        self.connectToNetwork(self._networkHAL.LOCAL_HOTSPOT_NAME,True)
                        EuclidConfigHelper.SetSSIDInConfig(self._networkHAL.LOCAL_HOTSPOT_NAME)
                        CsOobeHelper.StartOOBELiveNet()
                        self.RestartIPDiscovery()
                        
                    elif "/stop_service" in command:
                        # Stop publishing current ip
                        self.StopIPDiscovery()
                        self._run = False
                        
                    self._busy = False
                finally:# Resume connectivity monitoring.
                    self._busy = False                                          
                conn.close()
        except socket.error, e:
            print >>sys.stderr, 'Network Flow Socket Error: {}'.format(str(e.message))
            print "Error: " + str(e)
        except Exception as eX:
            print >>sys.stderr, 'Network Flow Socket Exception: {}'.format(str(eX.message))
        finally:
            self._sock.close()

   
    def _checkNetworkConnectivity(self):
        """
        Check if network is disconnected.
        If Yes then:           
            ** Check for how long
            ** If over the timeout defined: 
                Call Network fallback function
        else:
            wait for specified timeout.
        """
        while(self._run):
            try:                
                isConnected = False
                try:
                    isConnected = self._networkHAL.IsConnected()
                    isNetworkSameAsConfig = ( self._networkHAL.GetCurrentConnectionName() == EuclidConfigHelper.GetSSIDFromConfig())
                except Exception as eConnect:
                    print(str(eConnect))

                if (not self._busy and (isConnected is False or isNetworkSameAsConfig is False) and self._inSafeMode is False):
                    # Check time of disconnect and update if it was just discovered.
                    if(self._lastDisconnect is None):
                        self._lastDisconnect = datetime.now()
                    else:
                        # Check time between last disconnect and now.
                        if((datetime.now() -  self._lastDisconnect) > timedelta(seconds = self._disconnectTimeout)):
                            self._doNetworkFallback()
                else:
                    self._lastDisconnect = None # Reset last disconnection time.
                time.sleep(self._interval)
            except Exception as e:
                print(str(e)) # FIXME, Need logger.

    def _doNetworkFallback(self):
        """
        Fallback network to the default connection.
        """
        try:
            # Try reconnecting with existing network.
            res = self.connectToNetwork(EuclidConfigHelper.GetSSIDFromConfig(),False)
            # If reconnected we are done, Else fallback to 'Safe Mode'
            if (res is False):
                # load hotspot
                self.connectToNetwork(self._networkHAL.LOCAL_HOTSPOT_NAME,True)
                

                # Start Safe system in safe mode.
                CsOobeHelper.StartSafeMode()
                self._inSafeMode = True
            else:
                self._inSafeMode = False
        except Exception as e:
            print(str(e)) # FIXME, Need logger.

    def __del__(self):
        """
        Destructor
        """
        self._run = False

        if self._sock is not None:
            self._sock.close()

        if (self._networkHAL is not None):
            self._networkHAL = None
        
        if(self._serverThread is not None):
            self._serverThread = None
            
        self.StopIPDiscovery()   
            

################################### IP Discovery handling ######################################
        
    def StartIPDiscoverySender(self):
        """
        Call IP Discovery sender to send messages.
        """
        self._ipDiscoverySender.StartSending()

    def StopIPDiscovery(self):
        """
        Stop IP Discovery
        """
        if(self._ipDiscoverySender is not None):
            self._ipDiscoverySender.StopSending()
            self._ipDiscoverySender = None

    def RestartIPDiscovery(self):
        """
        Stop IP Discovery
        Call to Init new discovery sender.
        Start Sending messages.
        """
        if(self._ipDiscoverySender is not None):
            self._ipDiscoverySender.StopSending()
            self._ipDiscoverySender = None
        
        self._initIPDiscoveryService()
        self.StartIPDiscoverySender()

    def _initIPDiscoveryService(self):
        try:
            hostName = self._networkHAL.GetHostName()
            local_ip = self._networkHAL.GetCurrentIP()
            message = '{0}:{1}'.format(hostName,local_ip)
            multicast_ip = '224.1.1.100'
            multicast_port = 10000
            interval = 1
            
            # If service already run, stop it and only then create new one.
            if(self._ipDiscoverySender is not None):
                self._ipDiscoverySender.StopSending()
                self._ipDiscoverySender = None

            self._ipDiscoverySender =  DiscoverySender(message,local_ip,multicast_ip,multicast_port,interval)
            self._ipDiscoverySender.StartSending()
        except Exception as e:
            print('Init IP Discovery Sender Failed, Error: {}'.format(str(e.message))) # FIXME

################################# Flow Manager #######################################
    def scanNetworks(self):
            '''
            * Call for rescan of networks
            * Get current connection name.
            if currently connected to Hotspot:
                *** Stop IP Discovery sender
                *** Disconnect Hotspot.
                *** Run Rescan networks
                *** Save in available networks list.
                *** Reconnect to hotspot        
            Else:
                *** Run Rescan networks
                *** Save in available networks list.        
            '''
            try:
                print('Start Network Scan')
                SpeechClientFacade.RequestSay('Starting Network Scan, Please Wait')

                availablenetworkList = AvailableNetworkList()
                currentNetwork = self._networkHAL.GetCurrentConnectionName()
                if(currentNetwork == self._networkHAL.LOCAL_HOTSPOT_NAME):
                    print('Current network: ' + currentNetwork)
                    
                    # Stop IP Discovery
                    self.StopIPDiscovery()

                    print('Calling Network Disconnect')

                    disOut = self._networkHAL.DisconnectNetwork(currentNetwork)

                    # Wait for network to disconnect.       
                    print('After Disconnect, Wait Before Scan.')
                    time.sleep(15) 

                    # Handle in try catch so report erros if needed, but do try reconnect after.
                    try:
                        print "Scanning..."
                        wifiList = self._networkHAL.RescanNetworks()
                        print "done scanning, updating network list"
                        availablenetworkList.SetNetworkList(wifiList)
                        print('After Rescan')
                    except Exception as eScan:
                        print "Exception !"
                        print >>sys.stderr, 'Scan Networks Failed, Error: {0}'.format(str(eScan))                    
                    
                    print "Connecting to network"
                    time.sleep(2)
                    self.connectToNetwork(currentNetwork,True)

                    # Restart IP Discovery 
                    self.RestartIPDiscovery()  
		 
                    SpeechClientFacade.RequestSay('Network Scan Done')
		
                else:
                    wifiList = self._networkHAL.RescanNetworks()
                    availablenetworkList.SetNetworkList(wifiList)
                    SpeechClientFacade.RequestSay('Network Scan Done')
                    print('After Rescan')
            except Exception as e:
                SpeechClientFacade.RequestSay('Network Scan Failed')                
                print >>sys.stderr, 'Scan Networks Failed, Error: {}'.format(str(e.message))
                res = connectToNetwork(currentNetwork)
                if not res:
                    connectToNetwork(self._networkHAL.LOCAL_HOTSPOT_NAME,True)
                    
  	    SpeechClientFacade.Notify()
   
    
    def connectToNetwork(self, ssid, force = False):
        '''
            connecting to already saved network
        '''

        self._networkHAL.ConnectWiFi()
        print "Connecting to: " + ssid
        currentNetwork = self._networkHAL.GetCurrentConnectionName()
        
        if currentNetwork == ssid:
            print "Already connected"
            return True
        
        # check if network is saved
        savedNetworks = self._networkHAL.GetRegisteredNetworks()
        if ssid not in savedNetworks:
            print "Network is not saved"
            return False
        
        # Connecting to network!
        res = False
        while res == False:
            try:
		try: 
			self._networkHAL.ResetWiFi()
		except  Exception as eR:
			print >>sys.stderr, 'Reset Wifi Error: {}. Ignoring and reconnecting'.format(str(eR.message)) 
                self._networkHAL.ReconnectNetwork(ssid)
                print "Connected!"
                res = True
            except  Exception as eR:
                 print >>sys.stderr, 'Reconnect To Network Failed, Error: {}'.format(str(eR.message))
                 if not force:
                    print "Couldn't connect, aborting"
                    break
                 print "Couldnt connect, retrying"
        
        return res
        
        
    def connectToNewNetwork(self, ssid, passwd):
        '''
            connecting to already saved network
        '''
        print "Connecting to: " + ssid
        currentNetwork = self._networkHAL.GetCurrentConnectionName()
        if currentNetwork == ssid:
            print "Already connected"
            return True
        
        if(currentNetwork == EuclidNetworkHAL.LOCAL_HOTSPOT_NAME):
            print "Disconnecting from hotspot"
            disOut = self._networkHAL.DisconnectNetwork(currentNetwork)
            time.sleep(5)
        print "checking if network is available..."
        #wifiList = AvailableNetworkList().GetAvailableNetworks()
        #if ssid in wifiList:
        print "Trying to connect.."
        out, error = self._networkHAL.ConnectToNetwork(ssid,passwd)
        time.sleep(2)

        # If no error in register network...
        if (error is None or error == ''):
        # Update SSID in config file.
            print "Connected to new network!"
            #EuclidConfigHelper.SetSSIDInConfig(ssid)                        
        # Restart OOBE.
            #CsOobeHelper.StartOOBELiveNet()
        # Restart IP Discovery 
            #self.RestartIPDiscovery()
            return True
        else:
            print "Error connecting to new network"
            return False
                
       

    

if __name__ == '__main__':
    cs = CsConnectivityMonitor()
    cs._checkNetworkConnectivity()

    

