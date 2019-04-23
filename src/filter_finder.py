"""
This script is a diagnostic tool intended for the manual determination of what color ranges can be used to threshold out all pixels corresponding to a specific skateboard in videos (or snippets of videos) in which a single skateboard is filmed under controlled, static lighting conditions.

As of 04/22/2019: In order to use this script properly, the values for path, lower_chosen, and upper_chosen must be manually edited into this code.

TODO: make this script configurable to run from the commandline with no need to edit code, e.g. through `python board_filter -v "board.mp4" -c "wheels"`

This script was created as part of a school project, and therefore license-free.
"""

import os.path
import cv2
import numpy as np

__author__ = "Nick"


#Increments by which values can be changed through keyboard controls
sinc = 1
binc = 5

path = 'We have to manually enter the path to the video file here until we add support for commandline parameters.' #TODO: make path passable from the commandline

#if path leads to valid file
if os.path.isfile(path):
	cap = cv2.VideoCapture(path)
	
	#try to read first frame
	success, frame = cap.read()
	
	if(success):
		#get dimensions of this video
		height, width, _ = frame.shape

		#lower and upper bounds for color detections, to be derived using keyboard controls. The default values given here are the averages of previous trials with Steve's skateboard.
		lower_board = np.array([82,39,80])
		upper_board = np.array([100,155,180])

		lower_wheel = np.array([10,40,0])
		upper_wheel = np.array([29,230,255])

		lower_edge = np.array([10,25,115])
		upper_edge = np.array([25,155,255])

		#decide which color range to experiment on during this run
		lower_chosen = lower_edge
		upper_chosen = upper_edge

		#factor by which to downsample each frame
		scale = 2

		#go through all the frames of this video
		while(success):
			#rescale frame for faster processing
			frame = cv2.resize(frame, (width / scale, height / scale))
			
			#convert frame to HSV for easier processing
			hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			
			#get masks for individual board features
			board_mask = cv2.inRange(hsv_frame, lower_board, upper_board)
			wheel_mask = cv2.inRange(hsv_frame, lower_wheel, upper_wheel)
			edge_mask = cv2.inRange(hsv_frame, lower_edge, upper_edge)
			
			#combine feature masks into one
			skateboard_mask = cv2.bitwise_or(board_mask, wheel_mask)
			skateboard_mask = cv2.bitwise_or(skateboard_mask, edge_mask)
			
			#Extract features from frame using masks
			extracted_board = cv2.bitwise_and(frame, frame, mask = board_mask)
			extracted_wheel = cv2.bitwise_and(frame, frame, mask = wheel_mask)
			extracted_edge = cv2.bitwise_and(frame, frame, mask = edge_mask)
			extracted_skateboard = cv2.bitwise_and(frame, frame, mask = skateboard_mask)
			
			#show raw frame
			cv2.imshow('raw frame', frame)

			#show all extracted features
			cv2.imshow('extracted board', extracted_board)
			cv2.imshow('extracted wheels', extracted_wheel)
			cv2.imshow('extracted edges', extracted_edge)
			cv2.imshow('extracted skateboard', extracted_skateboard)
			
			#exit early if escape key pressed
			k = cv2.waitKey(5) & 0xFF
			if k == 27:
				break

			#keyboard controls for altering the lower bounds of experimental color range
			if k == ord('a'):
				lower_chosen[0] = (lower_chosen[0] + sinc) % 256
			if k == ord('s'):
				lower_chosen[1] = (lower_chosen[1] + sinc) % 256
			if k == ord('d'):
				lower_chosen[2] = (lower_chosen[2] + sinc) % 256
			if k == ord('z'):
				lower_chosen[0] = (lower_chosen[0] - sinc) % 256
			if k == ord('x'):
				lower_chosen[1] = (lower_chosen[1] - sinc) % 256
			if k == ord('c'):
				lower_chosen[2] = (lower_chosen[2] - sinc) % 256
				
			if k == ord('A'):
				lower_chosen[0] = (lower_chosen[0] + binc) % 256
			if k == ord('S'):
				lower_chosen[1] = (lower_chosen[1] + binc) % 256
			if k == ord('D'):
				lower_chosen[2] = (lower_chosen[2] + binc) % 256
			if k == ord('Z'):
				lower_chosen[0] = (lower_chosen[0] - binc) % 256
			if k == ord('X'):
				lower_chosen[1] = (lower_chosen[1] - binc) % 256
			if k == ord('C'):
				lower_chosen[2] = (lower_chosen[2] - binc) % 256

			#keyboard controls for altering the upper bounds of experimental color range
			if k == ord('g'):
				upper_chosen[0] = (upper_chosen[0] + sinc) % 256
			if k == ord('h'):
				upper_chosen[1] = (upper_chosen[1] + sinc) % 256
			if k == ord('j'):
				upper_chosen[2] = (upper_chosen[2] + sinc) % 256
			if k == ord('b'):
				upper_chosen[0] = (upper_chosen[0] - sinc) % 256
			if k == ord('n'):
				upper_chosen[1] = (upper_chosen[1] - sinc) % 256
			if k == ord('m'):
				upper_chosen[2] = (upper_chosen[2] - sinc) % 256

			if k == ord('G'):
				upper_chosen[0] = (upper_chosen[0] + binc) % 256
			if k == ord('H'):
				upper_chosen[1] = (upper_chosen[1] + binc) % 256
			if k == ord('J'):
				upper_chosen[2] = (upper_chosen[2] + binc) % 256
			if k == ord('B'):
				upper_chosen[0] = (upper_chosen[0] - binc) % 256
			if k == ord('N'):
				upper_chosen[1] = (upper_chosen[1] - binc) % 256
			if k == ord('M'):
				upper_chosen[2] = (upper_chosen[2] - binc) % 256
				
			#keyboard controls to reset experimental color range
			if k == ord('r'):
				lower_chosen[0] = 0
				lower_chosen[1] = 0
				lower_chosen[2] = 0
				upper_chosen[0] = 255
				upper_chosen[1] = 255
				upper_chosen[2] = 255

			#advance frame
			success, frame = cap.read()
			
		cv2.destroyAllWindows()

		#print out final values of experimental parameters once program is terminated
		print "Parameters derived during this run:"
		print "\r\n---Lower and upper bounds on color range:"
		print "[{},{},{}]".format(lower_chosen[0], lower_chosen[1], lower_chosen[2])
		print "[{},{},{}]".format(upper_chosen[0], upper_chosen[1], upper_chosen[2])
	
	else: print "The file provided could not be read. Make sure the given path leads to a video file."
	
else: print "please enter a valid filepath."