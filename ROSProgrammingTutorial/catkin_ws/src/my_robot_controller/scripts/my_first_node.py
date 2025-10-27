#!/usr/bin/env python3
import rospy 

# this is Hello World script!
if __name__ == "__main__":
    rospy.init_node("test_node")

    rospy.loginfo("Hello from test node")
    rospy.logwarn("This is a warning")
    rospy.logerr("This is an error")
    # rospy.debug("This is a debug info")

    rospy.sleep(1)
    rospy.loginfo("End of program")