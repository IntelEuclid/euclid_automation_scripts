#!/bin/bash
source /intel/euclid/config/settings.bash
source $ROS_INSTALL_DIR/setup.bash
source $CATKIN_WORKSPACE_DIR/devel/setup.bash
source $EUCLID_ROOT/config/ros_settings.bash
source /home/euclid/.bashrc
#export PYTHONPATH=/home/ros/catkin_ws/devel/lib/python2.7/dist-packages:/opt/ros/kinetic/lib/python2.7/dist-packages:/home/ros/libs/python-wifi-0.6.1:/home/ros/libs/python-wifi-0.6.1
export "DISPLAY=:0"

echo '*****'
echo $0 $1 $2 $3 $4
$1 $2 $3 $4 

exit 0
