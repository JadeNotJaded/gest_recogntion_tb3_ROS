#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

#global variables
cmd = ''
distance_ahead = 0
vel_msg = Twist()

def getDistanceAhead(msg):
    distance_ahead = msg.ranges[len(msg.ranges)/2]

def getCommand(msg):
    cmd = msg
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    if cmd == 'palm': #stop
           vel_msg.linear.y = 0
    elif cmd == 'thumb': #move forward
        vel_msg.linear.x = 0.1
    elif cmd == 'l': #turn 1 degree left
        vel_msg.angular.z = -0.1
        vel_msg.linear.x = 0.1
    elif cmd == 'c': #turn 1 degree right
        vel_msg.angular.z = 0.1
        vel_msg.linear.x = 0.10

def isSafe(command):
    if(distance_ahead < 10):
        return False
    return True

if __name__ == "__main__":
    #init node
    rospy.init_node('instruction')
    rospy.Subscriber('/command', String, getCommand)
    scan_sub = rospy.Subscriber('scan', LaserScan, getDistanceAhead)
    twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1) 
    if(isSafe(cmd)):
        twist_pub.publish(vel.msg)
    else:
        twist_pub
    rospy.spin()