import cv2
import numpy as np
import os
import random

# Frame Ripper Script WIP
# Working on adding subset functionality in order to randomly grab sets of frames instead of all of them

__author__ = 'Steve'

# Function to scan the video files, processes and adds them to Array video_list
def get_video_files(video_path = 'Videos'):
    
    entries = os.listdir(video_path)
    video_list = []
    
    for entry in entries:
        video_list.append(video_path + "/" + entry)
    return video_list

# Function that takes each element from the video_list and returns the total frame count of each video file
def get_total_frames(videos = get_video_files()):
    
    total_frames = []
    
    for index, file_name in enumerate(videos):
        cap = cv2.VideoCapture(file_name)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        total_frames.append(frame_count)
    return total_frames

# Video Processing
def process_video():
    
    # howdy partner
    # video shit goes here yo
    
    return

# Sub-set function
def sub_set_finder(cap, frames):  
    
    # Gets the total frames from the video
    for index, element in enumerate(frames):
        total_frames = element
                    
        # Sets the subset of frames to capture
        sub_set = int(random.random() * total_frames)
    
    return sub_set

    
    
# Master Function: Rips frames and creates seperate directories for each individual video
def rip_frames(vids = get_video_files(), frames = get_total_frames()):
    
    
    # Start of loop to run through each video held in the list
    for index, file_name in enumerate(vids):
        
        cap = cv2.VideoCapture(file_name)
                                         
        # Checks to see if that video has an corresponding image directory
        try:
            if not os.path.exists(file_name + 'data'):
                os.makedirs(file_name + 'data')
        except OSError:
            print ('Error: Creating directory')
            
        # Instantiates frame counter
        current_frame = 0
        
        # Starts frame capture
        while(True):
            
            # Sets boundaries for total images created per video
            if(current_frame <= 100):
                
                sub_set = sub_set_finder(cap, frames)
                
                # Sets the image to be read to the randomly selected frame from the subset
                cap.set(1, sub_set)
                # Capture = sub set of frames from current video
                ret, sub_set = cap.read()
                # Checks to see if cap can even be retrieved
                if not ret:        
                 #if no ret, break the loop
                 break 
                    
                # Saves image of the current frame in jpg file
                name = './'+ file_name +'data/image' + str(current_frame) + '.jpg'
                print ('Creating...' + name)   
                cv2.imwrite(name, sub_set)
                    
                # Counter to keep track of frames processed
                current_frame += 1
            else:
                #Breaks after each video file
                break
                
        # When everything done, releases the capture
        cap.release()
        cv2.destroyAllWindows()
        

# Calls master rip function
def main(run = rip_frames()):
    run
    
# Call to main
main()