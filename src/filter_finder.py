"""
This class is a diagnostic tool used for the manual determination of what color 
ranges can be used to threshold out all pixels corresponding to a specific
semantic features in videos (or snippets of videos) in which a single thing is 
filmed under controlled, static lighting conditions.
"""

import os.path
import cv2
import numpy as np

__author__ = 'Nick'

class FilterFinder:

	# TODO: add some basic validation and related exception handling (?)
	def __init__(self, unknown_filters = None, known_filters = None):
		# Increments by which values can be changed through keyboard controls
		self.increments = [1, 5]

		# quadruples of (control key, H/S/V channel index, sign of increment/decrement,
		# index of increment to use
		self.lower_controls = [	('a', 0, 1, 0),
								('s', 1, 1, 0),
								('d', 2, 1, 0),
								('z', 0, -1, 0),
								('x', 1, -1, 0),
								('c', 2, -1, 0),

								('A', 0, 1, 1),
								('S', 1, 1, 1),
								('D', 2, 1, 1),
								('Z', 0, -1, 1),
								('X', 1, -1, 1),
								('C', 2, -1, 1)]

		self.upper_controls = [	('g', 0, 1, 0),
								('h', 1, 1, 0),
								('j', 2, 1, 0),
								('b', 0, -1, 0),
								('n', 1, -1, 0),
								('m', 2, -1, 0),

								('G', 0, 1, 1),
								('H', 1, 1, 1),
								('J', 2, 1, 1),
								('B', 0, -1, 1),
								('N', 1, -1, 1),
								('M', 2, -1, 1)]
		
		# initialize filters 
		self.filters = {}
		if unknown_filters is not None:
			self.set_filters(self.add_filter_maps(unknown_filters))
		if known_filters is not None:
			self.set_filters(known_filters)
		# if both of the above conditions failed, use generic filter names
		if self.filters == {}:
			self.filters = self.add_filter_maps('filter1', 'filter2')

	# display video at path and allow user to alter chosen color range live
	# TODO: chunk this method into smaller methods because it's pretty long
	# TODO: implement optional writing
	def find_filter(self, path, chosen, downsize_scale = 2, write = True):
		# if desired parameter exists in filtering parameter set
		if chosen in self.filters:
			# decide which color filter bounds to alter using controls based on supplied name
			lower_chosen, upper_chosen = self.filters[chosen][0], self.filters[chosen][1]
			
			# loop through video repeatedly until user is satisfied with filter params	
			done = 'n'
			while done != 'y':
				# try to read file
				cap = cv2.VideoCapture(path)
				success, frame = cap.read() #TODO: refactor so that manually setting success isn't needed
				if success:
					# get dimensions of this video
					height, width, _ = frame.shape
					scaled_height, scaled_width = height/downsize_scale, width/downsize_scale

					# parameters for displaying filter parameters on extracted frames
					font = cv2.FONT_HERSHEY_SIMPLEX
					font_position = (50, scaled_height - 40)
					font_scale = .5
					font_color = (0,0,255)
					font_thickness = 2
					
					# dictionary of all extracted features to be displayed during runtime
					features = {}
					# dictionary of all binary masks used to extract those features
					masks = {}
					
					# go through all the frames of this video, displaying extracted features
					while success:
						# rescale frame for faster processing
						frame = cv2.resize(frame, (scaled_width, scaled_height))
						hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
						
						features['raw'] = frame
						
						# get all masks and features for each filter
						for key, (lower, upper) in self.filters.iteritems():
							# create mask
							masks[key] = cv2.inRange(hsv_frame, lower, upper)
							# extract feature using mask
							feature = cv2.bitwise_and(frame, frame, mask = masks[key])
							
							# write current filter info onto each filtered feature
							lower_text = 'lower: [{0},{1},{2}]'.format(lower[0], lower[1], lower[2])
							upper_text = 'upper: [{0},{1},{2}]'.format(upper[0],upper[1],upper[2])
							cv2.putText(feature, lower_text, font_position, font, font_scale, font_color, font_thickness)
							cv2.putText(feature, upper_text, (font_position[0], font_position[1]-30), font, font_scale, font_color, font_thickness)

							features[key] = feature

						# reset combined mask before recalculating it
						# TODO: find a way around having to do this
						masks['combined'] = 0
						masks['combined'] = self.combine_masks(masks)
						
						features['combined'] = cv2.bitwise_and(frame, frame, mask = masks['combined'])
						
						# show all things
						for key, feature in features.iteritems():
							cv2.imshow(key, feature)
						
						# exit early if escape key pressed
						k = cv2.waitKey(5) & 0xFF
						if k == 27:
							break

						# use defined keyboard controls to update upper and lower bounds of chosen color range

						# update lower bounds
						for key, channel, sign, increment in self.lower_controls:
							if k == ord(key):
								lower_chosen[channel] = (lower_chosen[channel] + (sign * self.increments[increment])) % 256
						# update upper bounds
						for key, channel, sign, increment in self.upper_controls:
							if k == ord(key):
								upper_chosen[channel] = (upper_chosen[channel] + (sign * self.increments[increment])) % 256
						
						# keyboard controls to reset experimental color range
						if k == ord('r'):
							lower_chosen[:] = 0
							upper_chosen[:] = 255
						if k == ord('R'):
							lower_chosen[:] = 0
							upper_chosen[:] = 0

						# advance frame
						success, frame = cap.read()
				# TODO: implement actual exception/error handling
				else: 
					print 'The file provided could not be read. Make sure the given path leads to a video file.'
					return None
				print "Satisfied with current filter params for {0}? (y/n)".format(chosen)
				done = raw_input()
			cv2.destroyAllWindows()
			
			return [lower_chosen, upper_chosen]

		else: 
			print ('The desired filtering parameter \'{0}\' was not found '+
			'in the parameter set:\r\n{1}').format(chosen, self.filters.keys())
	
	# do find_filter on all supplied filters, or all filters by default
	# TODO: implement optional writing
	def find_filters(self, path, chosen = None, downsize_scale = 2, write = True):
		if os.path.isfile(path):
			if chosen is not None:
				filters = chosen
			else: filters = self.filters
			for key in filters:
				print 'currently finding: {0}'.format(key)
				derived = self.find_filter(path, key, downsize_scale = downsize_scale, write = write)
				print '\t = {0}'.format(derived)
			return self.export_params()
		else: print 'The supplied filepath \'{0}\' did not lead to a file.'.format(path)

	# return a set of predetermined filters based on the trials using Steven's skateboard
	def get_default_filters(self):
		return {'board': [np.array([82,39,80]), np.array([100,155,180])], 
			'wheel': [np.array([10,40,0]),np.array([29,230,255])],
			'edge': [np.array([10,25,115]), np.array([25,155,255])]}
	
	# map a single name, or list of names to a default set of filter parameters
	def add_filter_maps(self, names, min_style_default = True):
		# decide which range to copy into all filters by default
		default = []
		if min_style_default is False:
			default = [[0,0,0], [255,255,255]]
		else: default = [[0,0,0], [0,0,0]]
		
		# if names is not list, put names into list
		# TODO: is this solution actually problematic?
		if not isinstance(names, list):
			names = [names]
		
		# map names to generic filter parameters
		filters = {}
		for name in names:
			filters[name] = [np.array(default[0][:]), np.array(default[1][:])]
		return filters
		
	def export_params(self):
		return self.filters

	# combine arbitrary number of binary masks into one
	def combine_masks(self, masks):
		combined_mask = []
		for key, mask in masks.iteritems():
			# initialize result mask to be first mask in dict if it doesn't already have a value
			# TODO: find a good solution to get rid of this ugly garbage solution
			if combined_mask == []:
				combined_mask = mask
				continue
			combined_mask = cv2.bitwise_or(combined_mask, mask)
		return combined_mask
	
	# overwrite this filter_finder's filters with a set of new filters
	def set_filters(self, filters):
		self.filters = {}
		for name, filter in filters.iteritems():
			self.filters[name] = filter

	# add all filters from a given dictionary of name: [lower, upper] to this instance's filters
	def add_filters(self, filters):
		for name, filter in filters.iteritems():
			self.filters[name] = filter
