#!/usr/bin/env python3
import rospy 
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist 
from turtlesim.srv import SetPen 

previous_x = 0

def call_set_pen_service(r, b, b, width, off):  # the params are coming from the commnads:
    # rosservice list 
    # rosservice info /turtle1/set_pen 
    # rossrv show turtlesim/SetPen 
    try:
        set_pen = rospy.ServiceProxy("/turtle1/set_pen", SetPen) # create a service client
        response = set_pen(r, g, b, width, off)
        # rospy.loginfo(response)
    except rospy.ServiceException as e:
        rospy.logwarn(e)

def pose_callback(pose: Pose):
    cmd = Twist()
    if pose.x > 9.0 or pose.x < 2.0 or pose.y > 9.0 or pose.y < 2.0:
        cmd.linear.x = 1.0
        cmd.angular.z = 1.4
    else:
        cmd.linear.x = 5.0
        cmd.angular.z = 0.0 

    pub.publish(cmd)

    global previous_x 
    if pose.x >= 5.5 and previous_x < 5.5:
        rospy.loginfo("Set color to red!")
        call_set_pen_service(255, 0, 0, 3, 0)
    elif pose.x < 5.5 and previous_x >= 5.5:
        rospy.loginfo("Set color to green!")
        call_set_pen_service(0, 255, 0, 3, 0)
    previous_x = pose.x 

if __name__ == "__main__":
    rospy.init_node("turtle_controller")
    rospy.wait_for_service("/turtle1/set_pen")
    call_set_pen_service(255, 0, 0, 3, 0)
    pub = rospy.Publisher("/turtlesim/cmd_vel", Twist, queue_size=10)
        # rostopic list
        # rostopic info /turtlesim/cmd_vel 
    sub = rospy.Subscriber("/turtle1/pose", Pose, callable=pose_callback)
        # rostopic list to get the first param
        # rostopic info /turtle1/pose to get the second param 
    rospy.loginfo("Node has been started.")

    rospy.spin()
