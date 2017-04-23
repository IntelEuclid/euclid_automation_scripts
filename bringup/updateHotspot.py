#!/usr/bin/env python
import subprocess
import sys


def generateHotSpot(macAddress):
    hotSpotTemplate = None

    with open('hotspot_template', 'r') as f:
        hotSpotTemplate = f.read()

    formTemplateStr = hotSpotTemplate.replace('{MAC_ADDRESS}', macAddress.strip('\n')) 
    with open('/etc/NetworkManager/system-connections/hotspot', 'a') as f2:
        f2.write(formTemplateStr)
        f2.close()

def get_mac_address():
    '''
    Get current MAC address of wlan0 device
    :param req:
    :return: macAddress
    '''
    myMac = subprocess.Popen(["ifconfig wlan0 | head -n1 | tr -s ' ' | cut -d' ' -f5"],stdout=subprocess.PIPE, shell=True)
    (macAddress, errors) = myMac.communicate()
    myMac.stdout.close()
    return macAddress

if __name__ == '__main__':
    try:
        macAddress = get_mac_address()
        generateHotSpot (macAddress)
    except Exception:
        pass
