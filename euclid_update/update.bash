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


#2. run-update:
#    2.1. calls pre-install script
#            If failes, exit with error 1
#
#    2.2. calls install script
#            If failes, exit with error 2
#
#    2.3. calls post-install script
#            If failes, exit with error 3
#
#    2.4. If error >1, perform rollback. 
#            else if error == 1, return message to user
#            else return success.


baseDir="/intel/euclid"

echo "Logging into LOG.txt"

#### Start
# Close STDOUT file descriptor
exec 1<&-
# Close STDERR FD
exec 2<&-

# Open STDOUT as $LOG_FILE file for read and write.
rm LOG.txt
exec 1<>LOG.txt

# Redirect STDERR to STDOUT
exec 2>&1

#####


bash update/pre-install.bash $directory $baseDir
if [ $? -eq 0 ]
then
  echo "pre-install.bash ended with success"
else
  echo "pre-install.bash ended with error" >&2
   
  exec 1>&0

  exec 2>&0
  
  exit 1
fi

bash update/install.bash $directory $baseDir
if [ $? -eq 0 ]
then
  echo "install.bash ended with success"
else
  echo "install.bash ended with error" >&2
   
  exec 1>&0

  exec 2>&0
  
  exit 2
fi

bash update/post-install.bash $directory $baseDir
if [ $? -eq 0 ]
then
  echo "post-install.bash ended with success"
else
  echo "post-install.bash ended with error" >&2

  exec 1>&0

  exec 2>&0
  
  exit 3
fi

#####


#### END
exec 1>&0

exec 2>&0

exit 0
