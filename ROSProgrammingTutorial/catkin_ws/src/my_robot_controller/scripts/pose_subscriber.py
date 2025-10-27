#!/usr/bin/env pythbon3
import rospy 
from geometry_msgs.msg import Twist 
from turtlesim.msg import Pose # since we are using this msg type, we need to make the tuttlesim is in the package.xml


def pose_callback(msg: Pose):
    rospy.loginfo("(" + str(msg.x) + ", " + str(msg.y) + ")")


if __name__ == "__main__":
    rospy.init_node("turtle_pose_subscriber") # turtle_pose_subscriber is the name of the node

    # rostopic list 
    # rostopic info /turtle1/pose
    # rosmsg show /turtlesim/Pose
    sub = rospy.Subscriber("/turtle1/pose", Pose, callback=pose_callback) # /turtle1/pose is the name of the topic

    rospy.loginfo("Node has been started")
    rospy.spin()