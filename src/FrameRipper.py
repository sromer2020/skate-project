import cv2
import os
import random

# Frame Ripper Script

__author__ = 'Steve'

# Rips frames and creates seperate directories for each individual video
def main():
    frames_needed = 100
    for video_file_name in get_video_files():
        cap = cv2.VideoCapture(video_file_name)
        video_folder_name = video_file_name + 'data'
        create_data_directory(video_folder_name)
        
        total_frame_count = get_total_frames(cap)
        for i in range(frames_needed):
            name = './{}/image{}.jpg'.format(video_folder_name, i)
            save_random_frame(cap, total_frame_count, name)
            
        cap.release()
        cv2.destroyAllWindows()

# Function to scan the video files, processes and adds them to Array video_list
def get_video_files(video_path = 'Videos'):
    
    video_list = []
    
    for entry in os.listdir(video_path):
        video_list.append(video_path + '/' + entry)
    return video_list

def create_data_directory(video_folder_name):
    # Checks to see if that video has an corresponding image directory
    try:
        if not os.path.exists(video_folder_name):
            os.makedirs(video_folder_name)
    except OSError:
        print ('Error: Creating directory')

# Function that returns the total frame count of the video
def get_total_frames(video_cap):
    return int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Video Processing
def process_frame(frame):
    
    # howdy partner
    # video shit goes here yo
    
    return frame

def get_random_frame(total_frames):
    return int(random.random() * total_frames)

def save_random_frame(cap, total_frames_of_video, image_name):
    frame_number = get_random_frame(total_frames_of_video)
                
    # Sets the image to be read to the randomly selected frame
    cap.set(1, frame_number)
    
    ret, frame = cap.read()
    
    # Checks to see if cap can even be retrieved
    if not ret:
        return
    
    frame = process_frame(frame)
        
    # Saves image of the current frame in jpg file
    print ('Creating...' + image_name)   
    cv2.imwrite(image_name, frame)
    
if __name__ == '__main__':
    main()
