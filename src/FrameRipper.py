import cv2
import numpy as np
import os 

#Frame Ripper Script WIP
#Working on adding subset functionality in order to randomly grab sets of frames instead of all of them
#
#Steve

#Function to scan the video files, processes and adds them to Array video_list
def getVideoFiles():
    
    entries = os.listdir('Videos')
    video_list = []
    
    for entry in entries:
        video_list.append("Videos/" + entry)
    return video_list

#Function that takes each element from the video_list and returns the total frame count of each video file
def getTotalFrames():
    
    videos = getVideoFiles()
    total_frames = []
    
    for index, file_name in enumerate(videos):
        cap = cv2.VideoCapture(file_name)
        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        total_frames.append(frameCount)
    return total_frames

#Master Fucntion: Rips frames and creates seperate directories for each individual video
def ripFrames():
    
    #instantiates the list of videos
    vids = getVideoFiles()
    #instantiates the list of frame data (ISN'T CALLED ANYWHERE YET)
    frames = getTotalFrames()
    
    #start of loop to run through each video held in the list
    for index, file_name in enumerate(vids):
        
        cap = cv2.VideoCapture(file_name)
        
        #Checks to see if that video has an corresponding image directory
        try:
            if not os.path.exists(file_name + 'data'):
                os.makedirs(file_name + 'data')
        except OSError:
            print ('Error: Creating directory')
            
        #Instantiates frame counter
        currentFrame = 0
        
        #Starts frame capture
        while(True):
            
            #Capture frames from video
            ret, frame = cap.read()
            
            #Checks to see if cap can even be retrieved
            if not ret:
                 #if no ret, break the loop
                break 
                
            # Saves image of the current frame in jpg file
            name = './'+ file_name +'data/image' + str(currentFrame) + '.jpg'
            print ('Creating...' + name)   
            cv2.imwrite(name, frame)

            #Counter to keep track of frames processed
            currentFrame += 1

        # When everything done, releases the capture
        cap.release()
        cv2.destroyAllWindows()

#Calls master rip function
ripFrames()