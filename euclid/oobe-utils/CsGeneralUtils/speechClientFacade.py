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



################ Speech Disabled for now as spd-say blocks gst-play ########################
import sys

class SpeechClientFacade(object):
    @staticmethod
    def RequestSay(text):
        """
        Post message call to request to say sentence.
        """
        try:
            #import subprocess
            # subprocess.call(["killall -u 'euclid' speech-dispatcher"])
            # subprocess.call(['su euclid -c "speech-dispatcher -c unix_socket -S /tmp/my.sock"'])
            # subprocess.call(['SPEECHD_ADDRESS=unix_socket:/tmp/my.sock spd-say "$1 $()"',"_",text], shell=True)\
	    #subprocess.call(['spd-say "Foo"'], shell=True)
            return True  
        except Exception as e:
            print >>sys.stderr,'Request Say, Error: {}'.format(str(e.message))
            return False

    @staticmethod
    def Notify():
        """
        Post message call to request to say sentence.
        """
        try:
            import subprocess
	    subprocess.call(['python /intel/euclid/oobe-services/startup_services/S6FeedbackServer/soundClient.py P\$"/usr/share/sounds/ubuntu/notifications/Positive.ogg"'], shell=True)
            return True  
        except Exception as e:
            print >>sys.stderr,'Notify, Error: {}'.format(str(e.message))
            return False

    @staticmethod
    def NotifyStart():
        """
        Post message call to request to say sentence.
        """
        try:
            import subprocess
	    subprocess.call(['python /intel/euclid/oobe-services/startup_services/S6FeedbackServer/soundClient.py P\$"/usr/share/sounds/ubuntu/notifications/Mallet.ogg"'], shell=True)
            return True  
        except Exception as e:
            print >>sys.stderr,'Notify, Error: {}'.format(str(e.message))
            return False

if __name__ == '__main__':
    SpeechClientFacade.RequestSay('hello')
    
