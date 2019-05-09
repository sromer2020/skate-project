"""
This script exists to store all the sets of filtering parameters we've derived
from our videos, and return those filters when prompted with a filename.
"""

import numpy as np
from image_filter import ImageFilter

__author__ = 'Nick'

# sets of filtering parameters to use with corresponding sets of video files
board_filters = {
        'board': [np.array([82,39,80]), np.array([100,155,180])], 
        'wheel': [np.array([10,40,0]),np.array([29,230,255])],
        'edge': [np.array([10,25,115]), np.array([25,155,255])]}
moving_filters = {
        'wheel': [np.array([0, 0, 0]), np.array([0, 0, 0])],
        'edge': [np.array([0, 0, 0]), np.array([0, 0, 0])],
        'board': [np.array([90, 80, 110]), np.array([105, 210, 255])]}
lot_filters = {
        'wheel': [np.array([0, 0, 0]), np.array([0, 0, 0])],
        'edge': [np.array([0, 0, 0]), np.array([0, 0, 0])],
        'board': [np.array([80, 24, 65]), np.array([100, 255, 255])]
}

# sets of files for which the defined filters filter out given object sufficiently well
board_files = ['board_Trim1.mp4', 'board_Trim2.mp4', 'board_Trim3.mp4', 'Grace1.MOV', 'Board1.mp4', 'Board2.mp4']
moving_files = ['moving_1.mp4', 'moving_2.mp4']
lot_files = ['still_1.mp4','still_2.mp4','still_3.mp4']

# files that, due to difficulties, can't be filtered very accurately through dumb color filters with no noise reduction
# TODO: add noise reduction to solve this
# TODO: add flat cropping around expected region of skateboard to solve this
invalid_files = ['Nick1.mp4','Nick2.mp4','Thomas1.mp4','Thomas2.mp4'] 

# 
chosen_filters = moving_filters
chosen_files = moving_files

# construct map of filenames:filters 
files_to_filters = {}
for filename in board_files:
    files_to_filters[filename] = board_filters
for filename in moving_files:
    files_to_filters[filename] = moving_filters
for filename in lot_files:
    files_to_filters[filename] = lot_filters

def get_filter_for_file(filename):
    return ImageFilter(files_to_filters[filename])
