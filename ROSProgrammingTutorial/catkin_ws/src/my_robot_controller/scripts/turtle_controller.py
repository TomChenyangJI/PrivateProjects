#!/usr/bin/env python3
import rospy 
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist 

def pose_callback(pose: Pose):
    cmd = Twist()
    if pose.x > 9.0 or pose.x < 2.0 or pose.y > 9.0 or pose.y < 2.0:
        cmd.linear.x = 1.0
        cmd.angular.z = 1.4
    else:
        cmd.linear.x = 5.0
        cmd.angular.z = 0.0 

    pub.publish(cmd)

if __name__ == "__main__":
    rospy.init_node("turtle_controller")
    pub = rospy.Publisher("/turtlesim/cmd_vel", Twist, queue_size=10)
        # rostopic list
        # rostopic info /turtlesim/cmd_vel 
    sub = rospy.Subscriber("/turtle1/pose", Pose, callable=pose_callback)
        # rostopic list to get the first param
        # rostopic info /turtle1/pose to get the second param 
    rospy.loginfo("Node has been started.")

    rospy.spin()
