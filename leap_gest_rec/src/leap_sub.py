#!/usr/bin/env python

import rospy     
from leap_motion.msg import leap     
from leap_motion.msg import leapros     
from geometry_msgs.msg import Twist, Point, Vector3 

def callback_ros(data):         
    global pub    
    twist = Twist()              
    ring = data.ring_tip  #subscribe to the Point value of the ring finger tip (left or right)       
    left_right = ring.x
    up_down = ring.y
    foward_backward = ring.z             
    twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0         
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0 

    # left and right
    twist.angular.z = left_right/250*-1
    #forward and backward
    twist.linear.x = foward_backward/500*-1

    #stop moving completely
    if(up_down < 100):
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0         
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0 

    pub.publish(twist)

def run():         
    global pub         
    rospy.init_node('leap_sub', anonymous=True)         
    rospy.Subscriber("/leapmotion/data", leapros, callback_ros)         
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)          
    rospy.spin()       
    
if __name__ == '__main__':      
    run() 