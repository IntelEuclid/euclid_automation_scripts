#!/bin/bash

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

source /intel/euclid/config/settings.bash
source $ROS_INSTALL_DIR/setup.bash

#### check whether, system is configured to connect to external network

# wait till network manager is ready

if [ $1 = "false" ]; then
    sleep 10
    
fi


NetworkName=`grep "ssid=" $EUCLID_ROOT/config/settings.ini | cut -d'=' -f2`
currentNetwork=`nmcli --fields NAME,DEVICE connection show --active | grep wlan0 | cut -f1 -d ' '`
status=0

echo "Current Network: $currentNetwork, to be: $NetworkName"
if ([ -z "$currentNetwork" ] || [ $currentNetwork != $NetworkName ]); then
  echo "Changing network"
  if [ $NetworkName = "hotspot" ]; then
      echo "Setting up hotspot.."
      nmcli connection up id hotspot
      status=$?
      echo "Done setting up hotspot!"
      
      
  else
      echo "Connecting to network: $NetworkName"
      nmcli connection up id $NetworkName
      status=$?
      if [ $status = 0 ]; then
          echo "Connected to $NetworkName"
      else
          echo "Failed to connect to $NetworkName, rolling back to hotspot"
	  sed -i '/'ssid'/c\'ssid='hotspot' $EUCLID_ROOT/config/settings.ini 

      fi
  fi



  #### if not or failed to connect to external network, open hotspot
  #nmcli con up id hotspot

  while [ $status != 0 ]; do
      sleep 2
      nmcli connection up id hotspot
      status=$?
      NetworkName="hotspot"
  done


  sleep 1

fi
#### check whether ROS MASTER URI is local IP address or remote
# generate ros_config.bash
# generate cs_ip.js
interface=`ifconfig | grep wlan | cut -f1 -d ' '`
ip_address=`ifconfig $interface | grep "inet addr:" | cut -d':' -f2 | cut -d' ' -f1`

if [ -z "$ip_address" ]; then
    ip_address="10.42.0.1"

fi

ros_master_uri=`grep "ROSMasterURI=" $EUCLID_ROOT/config/settings.ini | cut -d'=' -f2`

echo $ros_master_uri | grep localhost
is_local=$?
if [ $is_local != 0 ]; then
    echo "command: ROS_MASTER_URI=$ros_master_uri"
    export ROS_MASTER_URI=$ros_master_uri

    rosnode list  2>&1 | grep ERROR
    ret=$?
    if [ $ret = 0 ]; then
        echo "Remote ros master is not responding, running master on local machine"
        ros_master_uri="http://localhost:11311"
    fi
      
fi


echo "#!/bin/bash" > $EUCLID_ROOT/config/ros_settings.bash
echo "export ROS_MASTER_URI=$ros_master_uri" >>  $EUCLID_ROOT/config/ros_settings.bash
echo "export ROS_IP=$ip_address" >> $EUCLID_ROOT/config/ros_settings.bash



echo "var ros = new ROSLIB.Ros({" > $EUCLID_ROOT/public_html/js/lib/intel/cs_ip.js
echo "   url : 'ws://$ip_address:9090'" >> $EUCLID_ROOT/public_html/js/lib/intel/cs_ip.js
echo " });" >> $EUCLID_ROOT/public_html/js/lib/intel/cs_ip.js
echo "var system_ip = '$ip_address';" >> $EUCLID_ROOT/public_html/js/lib/intel/cs_ip.js


echo "define(['jquery'," > $EUCLID_ROOT/public_html/js/modules/components/global-settings.js
echo "        'underscore'" >> $EUCLID_ROOT/public_html/js/modules/components/global-settings.js
echo "], function ($, _) {" >> $EUCLID_ROOT/public_html/js/modules/components/global-settings.js

echo "    var GlobalSettings = {" >> $EUCLID_ROOT/public_html/js/modules/components/global-settings.js
echo "        timeoutInterval: 30000," >> $EUCLID_ROOT/public_html/js/modules/components/global-settings.js
echo "        system_ip: '$ip_address'," >> $EUCLID_ROOT/public_html/js/modules/components/global-settings.js
echo "        debug: false," >> $EUCLID_ROOT/public_html/js/modules/components/global-settings.js
echo "    };" >> $EUCLID_ROOT/public_html/js/modules/components/global-settings.js
echo "    return GlobalSettings;" >> $EUCLID_ROOT/public_html/js/modules/components/global-settings.js
echo "});" >> $EUCLID_ROOT/public_html/js/modules/components/global-settings.js

####
