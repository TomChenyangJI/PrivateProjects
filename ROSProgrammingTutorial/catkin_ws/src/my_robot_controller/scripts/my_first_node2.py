#!/usr/bin/env python3
import rospy 


# continuous Hello printout
if __name__ == "__main__":
    rospy.init_node("test_node")
    rospy.loginfo("Hello from test node")
    
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        rospy.loginfo("Hello")
        rate.sleep()