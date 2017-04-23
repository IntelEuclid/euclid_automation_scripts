# #!/usr/bin/env python

# ##################################################################################
# #Copyright (c) 2016, Intel Corporation
# #All rights reserved.
# #
# #Redistribution and use in source and binary forms, with or without
# #modification, are permitted provided that the following conditions are met:
# #
# #1. Redistributions of source code must retain the above copyright notice, this
# #list of conditions and the following disclaimer.
# #
# #2. Redistributions in binary form must reproduce the above copyright notice,
# #this list of conditions and the following disclaimer in the documentation
# #and/or other materials provided with the distribution.
# #
# #3. Neither the name of the copyright holder nor the names of its contributors
# #may be used to endorse or promote products derived from this software without
# #specific prior written permission.
# #
# #THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# #AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# #IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# #DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# #FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# #DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# #SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# #CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# #OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# #OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ##################################################################################

# import subprocess
# from CsAvailableNetworkList import AvailableNetworkList
# from ipDiscoverySender import DiscoverySender
# from EuclidNetworkHAL import EuclidNetworkHAL

# class CsNetworkController(object):
#     __instance = None
#     LOCAL_HOTSPOT_NAME = 'hotspot'
#     WIFI_DEVICE_NAME = 'wlan0'

#     def __new__(cls):
#         """
#         Init available networks collection, and scan for available networks.
#         """
#         if cls.__instance is None:
#             cls.__instance = super(CsNetworkController,cls).__new__(cls)
#             cls.__instance.__initialized = False
#         return cls.__instance

#     def __init__(self, runServer = False):
#         """
#         Init available networks collection, and scan for available networks.
#         """
#         if self.__initialized:
#             return
        
#         self._runServer = runServer
#         # self._ipDiscoverySender = None
#         self._networkHAL = EuclidNetworkHAL()
#         self._availableNetworkList = AvailableNetworkList()

#         if (self._runServer):
#             self.RescanNetworks()
#             # self._initIPDiscoveryService()
#             # self.StartIPDiscoverySender()
            
#         self.__initialized = True
        
#     def RescanNetworks(self):
#         '''
#         Call os to rescan wifi.
#         Get the updated list from os.
#         Update internal collection.
#         :raise: exception when operation returned errors.
#         '''
#         try:
#             wifiList = self._networkHAL.RescanNetworks()
#             self._availableNetworkList.SetNetworkList(wifiList)
#         except Exception as e:
#             raise e

#     # def GetAvailableNetworkList(self):
#     #     '''
#     #     Get the saved list of Available networks.
#     #     :return Tuple of last update time, and the collection of available networks.
#     #     :raise: exception when operation returned errors.
#     #     '''
#     #     try:
#     #         lastUpdateTime = self._availableNetworkList.GetLastUpdateTime()
#     #         wifiList = self._availableNetworkList.GetAvailableNetworks()
#     #         return lastUpdateTime, wifiList
#     #     except Exception as e:
#     #         raise e

# # ################################### IP Discovery handling ######################################
        
# #     def StartIPDiscoverySender(self):
# #         """
# #         Call IP Discovery sender to send messages.
# #         """
# #         self._ipDiscoverySender.StartSending()

# #     def StopIPDiscovery(self):
# #         """
# #         Stop IP Discovery
# #         """
# #         if(self._ipDiscoverySender is not None):
# #             self._ipDiscoverySender.StopSending()
# #             self._ipDiscoverySender = None

# #     def RestartIPDiscovery(self):
# #         """
# #         Stop IP Discovery
# #         Call to Init new discovery sender.
# #         Start Sending messages.
# #         """
# #         if(self._ipDiscoverySender is not None):
# #             self._ipDiscoverySender.StopSending()
# #             self._ipDiscoverySender = None
        
# #         if(self._runServer):
# #             self._initIPDiscoveryService()
# #             self.StartIPDiscoverySender()

# #     def _initIPDiscoveryService(self):
# #         try:
# #             hostName = self._networkHAL.GetHostName()
# #             local_ip = self._networkHAL.GetCurrentIP()
# #             message = '{0}:{1}'.format(hostName,local_ip)
# #             multicast_ip = '224.1.1.100'
# #             multicast_port = 10000
# #             interval = 0.5
            
# #             # If service already run, stop it and only then create new one.
# #             if(self._ipDiscoverySender is not None):
# #                 self._ipDiscoverySender.StopSending()
# #                 self._ipDiscoverySender = None

# #             self._ipDiscoverySender =  DiscoverySender(message,local_ip,multicast_ip,multicast_port,interval)
# #             self._ipDiscoverySender.StartSending()
# #             # return ipDiscoverySender
# #         except Exception as e:
# #             print('Init IP Discovery Sender Failed, Error: {}'.format(str(e.message))) # FIXME


# if __name__ == '__main__':
#     csNC = CsNetworkController()
#     print('hello')