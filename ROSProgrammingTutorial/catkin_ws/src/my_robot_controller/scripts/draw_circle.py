#!/usr/bin/env python3
import rospy 
from geometry_msgs.msg import Twist

if __name__ == "__main__":
    rospy.init_node("draw_cricle")
    rospy.loginfo("Node has been started.")

    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10) # here i need to change the package.xml file

    rate = rospy.Rate(2)

    while not rospy.is_shutdown():
        #
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.x = 1.0
        pub.publish(msg)
        rate.sleep()

