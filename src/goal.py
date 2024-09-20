#!/usr/bin/env python3
#Determine your interpreter
#Including Libraries
import rospy #Including functions of ROS related to python
from geometry_msgs.msg import Twist  #Include Twist message type from geometry messages library
from turtlesim.msg import Pose #Include Pose message type from turtlesim.msg library
import math #importing math functions

# Initialize global variables (current_pose)
current_pose = Pose()

def pose_callback(data): #define callback function
    global current_pose #To use the global variable current_pose
    current_pose = data #Takes what's inside the message (data) and puts it into variable current_pose

def move_to_goal(x_goal, y_goal): 
    global current_pose

    rospy.init_node('turtle_move_to_goal', anonymous=True) #initialising node
    #anonymous to make node have different names if by mistake you named 2 nodes or more the same name
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) #initialize publisher
    #You need to include message type (Write what's after the IMPORT above
    sub = rospy.Subscriber('/turtle1/pose', Pose, pose_callback) #initialize subscriber
    #Callback is initiated when message is sent on the topic /turtle1/pose
    rate = rospy.Rate(10) #define rate in which messages will be sent

    goal_pose = Pose() #Create object from class called Pose
    #Equate goal_pose to required x & y co-ordinates for turtlesim to go to
    goal_pose.x = x_goal 
    goal_pose.y = y_goal

    vel_msg = Twist() #Creating an object from class 

    while not rospy.is_shutdown():
        # Calculate the distance to the goal
        distance = math.sqrt((goal_pose.x - current_pose.x)**2 + (goal_pose.y - current_pose.y)**2)

        # Calculate the linear velocity
        vel_msg.linear.x = 1.5 * distance

        # Calculate the angle to the goal
        angle_to_goal = math.atan2(goal_pose.y - current_pose.y, goal_pose.x - current_pose.x)
        #To always make sure that angle_diff is always positive
        if (angle_to_goal>current_pose.theta):
            angle_diff = angle_to_goal - current_pose.theta
        if (current_pose.theta>angle_to_goal): 
             angle_diff = current_pose.theta - angle_to_goal


        # Calculate the angular velocity
        vel_msg.angular.z = 4.0 * angle_diff

        # Stop the turtle when it reaches the goal
        if distance < 0.01:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            pub.publish(vel_msg)
            break

        # Publish the velocity message
        pub.publish(vel_msg)
        rate.sleep()

if __name__ == '__main__': #defining main 
    try:
        #User enters x & y co-ordinates
        x_goal= float(input("Please enter value of x-coordinate"))
        y_goal= float(input("Please enter value of y-coordinate"))
        #Check that co-ordinates is within limits
        while (x_goal>=10 or y_goal >=10 or x_goal<0 or y_goal<0): 
            print("Please enter coordinates of x and y in the range of 0-10")
            x_goal= float(input("Please enter value of x-coordinate"))
            y_goal= float(input("Please enter value of y-coordinate"))
        move_to_goal(x_goal, y_goal) #Call function to move to co-ordinates entered
    except rospy.ROSInterruptException:
        pass
