/******************************************************************************
Copyright (c) 2016, Intel Corporation
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*******************************************************************************/

#include <ros.h>
#include <geometry_msgs/PointStamped.h>

ros::NodeHandle  nh;

//Callback function for the person tracking topic messges. 
void messageCb( const geometry_msgs::PointStamped& msg) {
  double personDistanceThreshold = 1;
  if(msg.point.z > 0 && msg.point.z < personDistanceThreshold )
  {
    digitalWrite(13, HIGH); //if data is valid and user is closer than the threshold, turn on the LED. 
  }
  else
  {
    digitalWrite(13, LOW); //turn OFF the LED if the data is not valid or user is too far.
  }
    
}

//Declaring person tracking subscriber with the topic name and the callback function
ros::Subscriber<geometry_msgs::PointStamped> sub_person_tracking("person_follower/goal", messageCb );

void setup() {
  //Initialize the node (needed by ROS)
  nh.initNode();
  //Subscribing to person tracking data
  nh.subscribe(sub_person_tracking);

  //LED
  pinMode(13, OUTPUT);
}

void loop() {
  nh.spinOnce(); //Allows ROS to run and to send/receive new messages.
}

