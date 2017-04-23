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

import subprocess
import EuclidConfigHelper
import time

class EuclidNetworkHAL(object):
    LOCAL_HOTSPOT_NAME = 'hotspot'
    WIFI_DEVICE_NAME = 'wlan0'

    def ConnectToNetwork(self, ssid, password):
        '''
        Call to to connect to known WiFi with ssid and password.
        Provide ssid and password.
        :return: process output, and or error if exists.
        '''
        nmcli = subprocess.Popen(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = nmcli.communicate()
        nmcli.stdout.close()
        return out, error

    def RescanNetworks(self):
        '''
        Call os to rescan wifi.
        Get the updated list from os.
        :return available wifi collection.
        :raise: exception when operation returned errors.
        '''
        try:
            wifiList = []

            # Call rescan
            #nmcliRescan = subprocess.Popen(["nmcli", "dev", "wifi","rescan"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		#iw dev wlan0 scan    
            nmcliRescan = subprocess.Popen(["iw", "dev", "wlan0","scan"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, error = nmcliRescan.communicate()
            nmcliRescan.stdout.close()

            if(self._hasErrors(error)):
                raise Exception('Rescan Networks Failed, Error {0}'.format(str(error)))

            # Get list
            nmcliList = subprocess.Popen(["nmcli", "-t", "--fields", "SSID", "dev", "wifi","list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            listProcOut, listProcError = nmcliList.communicate()
            nmcliList.stdout.close()

            if(self._hasErrors(listProcError)):
                raise Exception('Rescan Networks Failed Calling List, Error {0}'.format(str(error)))

            wifiList = filter(None, listProcOut.split("\n"))

            return wifiList
        except Exception as e:
            raise e
    
    def GetRegisteredNetworks(self):
        '''
        Get list of registered known connections.
        :return collection of registered networks
        :raise: exception when operation returned errors.
        '''
        try:
            wifiList = []
            nmcli = subprocess.Popen(
                ["nmcli", "-t", "--fields", "NAME", "con", "show"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            out, error = nmcli.communicate()
            nmcli.stdout.close()    

            if(self._hasErrors(error)):
                raise Exception('Get Registered Networks Failed, Error {0}'.format(str(error)))

            wifiList = filter(None, out.split("\n"))        
            return wifiList
        except Exception as e:
            raise e
    
    def ReconnectNetwork(self, ssid):
        '''
        Reconnect to an existing registerd WiFi.
        :return: process output.
        :raise: exception when operation returned errors.
        '''
        try:
            nmcli = subprocess.Popen(
                ["nmcli", "con", "up", "id", ssid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            out, error = nmcli.communicate()
            nmcli.stdout.close()    

            if(self._hasErrors(error)):
                raise Exception('Reconnect Network Failed, Error {0}'.format(str(error)))

            return out
        except Exception as e:
            raise e   

    def DisconnectNetwork(self, ssid):
        '''
        Disconnect from an existing WiFi
        :return: process output.
        :raise: exception if operation returned errors.
        '''
        try:
            nmcli = subprocess.Popen(["nmcli", "connection", "down", "id", ssid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, error = nmcli.communicate()
            nmcli.stdout.close()    

            if(self._hasErrors(error)):
                raise Exception('Disconnect Network Failed, Error {0}'.format(str(error)))
            
            return out
        except Exception as e:
            raise e

    def DisconnectWiFi(self):
        '''
        Disconnect WiFi
        :return: process output.
        :raise: exception if operation returned errors.
        '''
        try:
            nmcli = subprocess.Popen(["nmcli", "radio", "wifi", "off"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, error = nmcli.communicate()
            nmcli.stdout.close()    

            if(self._hasErrors(error)):
                raise Exception('Disconnect Network Failed, Error {0}'.format(str(error)))
            
            return out
        except Exception as e:
            raise e

    def ConnectWiFi(self):
        '''
        Connect WiFi
        :return: process output.
        :raise: exception if operation returned errors.
        '''
        try:
            nmcli = subprocess.Popen(["nmcli", "radio", "wifi", "on"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, error = nmcli.communicate()
            nmcli.stdout.close()    

            if(self._hasErrors(error)):
                raise Exception('Disconnect Network Failed, Error {0}'.format(str(error)))
            
            return out
        except Exception as e:
            raise e

    def ResetWiFi(self):
        '''
        Resets the WiFi
        :return: True if all went fine.
        :raise: exception if operation returned errors.
        '''
        try:
            self.DisconnectWiFi()
	    time.sleep(5)
	    self.ConnectWiFi()
            
            return True
        except Exception as e:
            raise e

    def GetMacAddress(self):
        '''
        Get current MAC address of wlan_xx device.
        Device (wlan_xx) name declared globaly. 
        :return: macAddress for specific device.
        :raise: exception if operation returned errors.
        '''
        try:
            myMac = subprocess.Popen(["ifconfig " + self.WIFI_DEVICE_NAME + "| head -n1 | tr -s ' ' | cut -d' ' -f5"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            (macAddress, error) = myMac.communicate()
            myMac.stdout.close()
            
            if(self._hasErrors(error)):
                raise Exception('Get Mac Address Failed, Error {0}'.format(str(error)))
            
            return macAddress 
        except Exception as e:
            raise e

    def GetCurrentIP(self):
        '''
        get current IP address
        :return: IP address.
        :raise: exception if operation returned errors.
        '''
        try:
            my_ip = subprocess.Popen(['ifconfig ' + self.WIFI_DEVICE_NAME +  ' | awk "/inet /" | cut -d":" -f 2 | cut -d" " -f1'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            (IP, error) = my_ip.communicate()

            if(self._hasErrors(error)):
                    raise Exception('Get IP Address Failed, Error {0}'.format(str(error)))

            IP = str(IP).rstrip('\r\n')
            my_ip.stdout.close()
            return IP
        except Exception as e:
            raise e

    def GetHostName(self):
        '''
        get current hostname.
        :return: string represents current hostname.
        :raise: exception if operation returned errors.
        '''
        try: 
            import socket
            hostname = socket.gethostname()
            return hostname
        except Exception as e:
            raise Exception('Get Host Name Failed, Error: {0}'.format(str(e.message)))

    def GetCurrentConnectionName(self):
        '''
        get current Connection name if connected
        :return: Connection name or empty if not connected.
        :raise: exception if operation returned errors.
        '''
        try:
            # myConnection = subprocess.Popen(['iw dev ' + EuclidNetworkHAL.WIFI_DEVICE_NAME + ' info | grep ssid | cut -d" " -f2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            myConnection = subprocess.Popen(['nmcli','--fields', 'NAME, DEVICE', 'connection', 'show', '--active'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, error = myConnection.communicate()

            if(self._hasErrors(error)):
                raise Exception('Get Current Connection Name Failed, Error {0}'.format(str(error)))

            rawList = filter(None, out.split("\n")) 
            connectionNames = filter(lambda x: str.strip(x) != 'NAME' and str.strip(x) != '' and self.WIFI_DEVICE_NAME in x, rawList)   
            connectionName = ''

            if(len(connectionNames) > 0): # FIXME
                connectionName = str.strip(connectionNames[0].split()[0])

            myConnection.stdout.close()
            return connectionName
        except Exception as e:
            raise e

    def IsConnected(self):
        '''
        Check if connected to network and compare connection name to ssid settings from config.
        Return: True if connected and equals to config, Otherwise False.
        :raise: exception if operation returned errors.
        '''
        try:
            currentConnection = self.GetCurrentConnectionName()
            currentSSIDFromConfig = EuclidConfigHelper.GetSSIDFromConfig()

            if(currentConnection is None or currentConnection == '' or currentConnection != currentSSIDFromConfig):
                return False
            else:
                return True
        except Exception as e:
            raise e

    def _hasErrors(self, error):
        """
        Check if error are None or Empty.
        """
        if(error is None or error == ''):
            return False
        else:
            return True

if __name__ == '__main__': 
    print 'hello'  
    item = EuclidNetworkHAL()

    item.GetCurrentConnectionName()
    # time.sleep(5)
