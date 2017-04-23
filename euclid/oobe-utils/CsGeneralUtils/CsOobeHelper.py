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
import sys
import time

def Reboot():
    try:
	subprocess.Popen(
            ['python /intel/euclid/oobe-services/startup_services/S6FeedbackServer/soundClient.py P\$"/usr/share/sounds/ubuntu/notifications/Mallet.ogg"'], shell=True)    
	time.sleep(3)    
	subprocess.call(['reboot'])
    except Exception as e:
        print >>sys.stderr, 'Reboot Failed, Error: {}'.format(str(e.message))

def Shutdown():
    try:
        subprocess.Popen(
            ['python /intel/euclid/oobe-services/startup_services/S6FeedbackServer/soundClient.py P\$"/usr/share/sounds/ubuntu/notifications/Mallet.ogg"'], shell=True)
	time.sleep(3)
        subprocess.call(['shutdown','-P','0'])
    except Exception as e:
        print >>sys.stderr, 'Shutdown Failed, Error: {}'.format(str(e.message))

def RestartOOBE():
    try:
	subprocess.Popen(
            ['python /intel/euclid/oobe-services/startup_services/S6FeedbackServer/soundClient.py P\$"/usr/share/sounds/ubuntu/notifications/Mallet.ogg"'], shell=True)
	#time.sleep(3)
        subprocess.call(['service','oobe-init','restart-oobe'])
    except Exception as e:
        print >>sys.stderr, 'Restart OOBE Failed, Error: {}'.format(str(e.message))

def RestartOOBELiveNet():
    try:
        subprocess.call(['service','oobe-init','restart-live-net'])
    except Exception as e:
        print >>sys.stderr, 'Restart OOBE Live Net Failed, Error: {}'.format(str(e.message))

def StopOOBELiveNet():
    try:
        subprocess.call(['service','oobe-init','stop-oobe-live-net'])
    except Exception as e:
        print >>sys.stderr, 'Stop OOBE Live Net Failed, Error: {}'.format(str(e.message))

def StartOOBELiveNet():
    try:
        subprocess.call(['service','oobe-init','start-oobe-live-net'])
    except Exception as e:
        print >>sys.stderr, 'Start OOBE Live Net Failed, Error: {}'.format(str(e.message))

def StartSafeMode():
    try:
        subprocess.call(['service','oobe-init','start-safe-mode'])
    except Exception as e:
        print >>sys.stderr, 'Start OOBE Live Net With safe mode, Error: {}'.format(str(e.message))

def ExitSafeMode():
    try:
        subprocess.call(['service','oobe-init','exit-safe-mode'])
    except Exception as e:
        print >>sys.stderr, 'Exit OOBE Live Net With safe mode, Error: {}'.format(str(e.message))
        
def GenerateArduinoLibrary():
    try:
        retVal = subprocess.call(['sh','/intel/euclid/oobe-utils/generateArduinoLibrary/generateArduinoLibrary.sh'])
        return retVal == 0 
    except Exception as e:
        print >>sys.stderr, 'Generate Arduino Library Failed, Error: {}'.format(str(e.message))  

def exportSettings():
    try:
        retVal = subprocess.call(['sh','/intel/euclid/oobe-utils/exportImportSettings/exportSettings.sh'])
        return retVal == 0
    except Exception as e:
        print >>sys.stderr, 'Export Settings Failed, Error: {}'.format(str(e.message))
