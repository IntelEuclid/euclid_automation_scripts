import re
import sys

SETTINGS_FILE_PATH = "/intel/euclid/config/settings.ini"

def GetSSIDFromConfig():
    try:
        file = open(SETTINGS_FILE_PATH,"r")

        for line in file:
            if re.search('ssid=',line):
                return str(line.split('=')[1]).rstrip()
    except Exception as e:
        raise e   

def SetSSIDInConfig(ssidName):
    try:
        import os
        cmd = "sed -i '/" + 'ssid' + "/c\'" + 'ssid=' +ssidName +  " " + SETTINGS_FILE_PATH
        os.system(cmd)
    except Exception as e:
        raise e   

if __name__ == '__main__':
    ssid = GetSSIDFromConfig()
    SetSSIDInConfig('hotspot')