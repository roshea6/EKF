#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import rospy

# IMU messages
from sensor_msgs.msg import Imu

# Depth sensor messages
from bar30_depth.msg import Depth

# DVL messages
from rti_dvl.msg import DVL

# Robot state message
from EKF.msg import robot_state

class Visualizer(object):
	# Initialization function to setup variables
	def __init__(self):
		# Initialize state as a blank robot_state message
		self.state = robot_state()

		# Fill in with dummy values
		self.state.x = 1
		self.state.y = 1
		self.state.z = 1
		self.state.roll = 1
		self.state.pitch = 1
		self.state.yaw = 1
		self.state.x_dot = 1
		self.state.y_dot = 1
		self.state.z_dot = 1
		self.state.roll_dot = 1
		self.state.pitch_dot = 1
		self.state.yaw_dot = 1

		# Variables to be used for the plot
		self.fig = plt.figure()
		self.ax1 = self.fig.add_subplot(1,1,1)

		# These will be replaced by more appropriately named lists later
		self.roll_ar = []
		self.pitch_ar = []
		self.yaw_ar = []
		self.time_ar = []

		self.started = False
		self.start_time = rospy.Time.now()

		# TODO: Make variables to contain data from the raw state that need to be plotted


	# Recieves messages directly from the IMU topic and plots it
	def rawStateCallback(self, imu_msg):
		pass

		# TODO: Add raw state data to proper variable

	# Recieves messages from the EKF node about the latest state
	def ekfStateCallback(self, state_msg):
		# print state_msg

		# Get the start time to make graphing look better
		if(self.started == False):
			self.start_time = rospy.Time.now()
			self.started = True

		# Update state with new message
		# We might not need this?
		self.state = state_msg

		# Append x and y from msg into roll_ar and pitch_ar
		self.roll_ar.append(state_msg.roll)
		self.pitch_ar.append(state_msg.pitch)
		self.yaw_ar.append(state_msg.yaw)

		self.time_ar.append(state_msg.header.stamp.secs - self.start_time.secs)

		



	# Plots the newest data from either the IMU or the EKF on the plot
	def plotData(self, data):
		# Clear the previous data
		self.ax1.clear()

		# Plot the new points
		self.ax1.plot(self.time_ar, self.roll_ar)

		# Plot x against z just to show two lines
		self.ax1.plot(self.time_ar, self.pitch_ar)

		# Plot x against z just to show two lines
		self.ax1.plot(self.time_ar, self.yaw_ar)

		# TODO: Add lines for data from raw state



if __name__ == "__main__":
	# Initialize the ROS node
	rospy.init_node("ekf_visualizer", anonymous=True)

	# Visualizer object which will be used to keep track of the robot state and plot it
	vis = Visualizer()

	# Subscriber for robot state topic
	rospy.Subscriber('/state', robot_state, vis.ekfStateCallback)

	# TODO: Setup subsriber for raw state

	# Set the figure to update every 1ms using the plotData function in the Visualizer class
	# The plotData function will clear the previous data and replot with any new data received
	# from the state callback functions
	ani = animation.FuncAnimation(vis.fig, vis.plotData, interval=1000)
	
	# Display the plot
	plt.show()

	rospy.spin()
