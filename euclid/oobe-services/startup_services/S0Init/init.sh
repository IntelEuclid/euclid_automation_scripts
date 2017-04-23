#!/bin/bash

##################################################################################
#Copyright (c) 2017, Intel Corporation
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

echo "Startup - S0 Init running!"
runFlagFile='/intel/euclid/oobe-services/startup_services/S0Init/firstRun'

if [ -f "$runFlagFile" ]; then
   boot_number=`cat $runFlagFile`
   if [ $boot_number == "1" ]; then
     #sleep 10
     #cp /intel/euclid/bios/CHTT_IFWI_X64_R_TS00_13_CS170208_SecEnabled_Production.fv /boot/efi/BIOSUPDATE.fv
     #sync
     #sleep 20
     echo "2" > /intel/euclid/oobe-services/startup_services/S0Init/firstRun
     reboot
   elif [ $boot_number == "2" ]; then
     sleep 15
     hostn=$(cat /etc/hostname)
     mac_addr=`ifconfig wlan0 | awk '/HWaddr/ {print  $5}'`
     echo "Mac address: $mac_addr"
     trimed_mac=`echo ${mac_addr^^} | cut -d ':' -f5,6  | tr  -d  ':'`
     newhost="EUCLID_${trimed_mac}"

     # Update hostname
     sed -i "s/$hostn/$newhost/g" /etc/hosts
     sed -i "s/$hostn/$newhost/g" /etc/hostname

     # Update hotspot
     sed -i "s/^ssid=.*/ssid=$newhost/g" /etc/NetworkManager/system-connections/hotspot
     sed -i "s/^mac-address=.*/mac-address=$mac_addr/g" /etc/NetworkManager/system-connections/hotspot
     
     echo "3" > /intel/euclid/oobe-services/startup_services/S0Init/firstRun
     
     echo 'System Will now reboot'
     sleep 3
     
     reboot
   elif [ $boot_number == "3" ]; then 
     /intel/euclid/oobe-services/startup_services/S0Init/load_calibration_from_bios.sh

     # Delete the file
     rm -rf $runFlagFile
     
     sync

   fi
fi





