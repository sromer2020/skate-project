"""
This script is intended to be used with the related filter_finder.py. It filters out all the pixels corresponding to a single skateboard in a given controlled video of a skateboard under static conditions.

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
			extracted_skateboard = cv2.bitwise_and(frame, frame, mask = skateboard_mask)
			
			#exit early if escape key pressed
			k = cv2.waitKey(5) & 0xFF
			if k == 27:
				break

			#advance frame
			success, frame = cap.read()
			
		cv2.destroyAllWindows()
	
	else: print "The file provided could not be read. Make sure the given path leads to a video file."
	
else: print "please enter a valid filepath."