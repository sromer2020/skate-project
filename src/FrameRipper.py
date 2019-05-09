import cv2
import os
import numpy as np

from filter_finder import FilterFinder
from image_filter import ImageFilter
from autocropper import AutoCropper

from argparse import ArgumentParser

# Frame Ripper Script

__author__ = 'Steve'

# Rips frames and creates seperate directories for each individual video
def main():
    parser = ArgumentParser()
    parser.add_argument('videospath', 
                        help='path to videos to rip and crop frames')
    parser.add_argument('--framecount', nargs='?', 
                        help='number of frames to rip for each video')
    args = parser.parse_args()
    
    frames_needed = int(args.framecount if args.framecount is not None else 500)
    generator = FilterFinder()
    skateboard_filter = ImageFilter(generator.get_default_filters())
    autocropper = AutoCropper(blur_amt=1000, padding=40, pre_crop=0, img_stride=3)
    
    for video_file_name in get_video_files(args.videospath):
        cap = cv2.VideoCapture(video_file_name)
        video_folder_name = video_file_name + 'data'
        create_data_directory(video_folder_name)
        
        total_frame_count = get_total_frames(cap)
        frames_to_use = get_random_frame_numbers(total_frame_count, frames_needed)
        for i, frame in enumerate(frames_to_use):
            name = os.path.join(video_folder_name, 'image{}.jpg'.format(i))
            save_random_frame(cap, frame, name, skateboard_filter, autocropper)
            
        cap.release()
        cv2.destroyAllWindows()

# Function to scan the video files, processes and adds them to Array video_list
def get_video_files(video_path = 'Videos'):
    
    video_list = []
    
    for entry in os.listdir(video_path):
        video_list.append(os.path.join(video_path, entry))
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
def process_frame(frame, image_filter, autocropper):
    mask = image_filter.get_aggregate_mask(frame)
    cropped_frame = autocropper.crop(frame, mask)
    return cropped_frame

def get_random_frame_numbers(total_frames, desired_number):
    all_numbers = np.array(range(total_frames))
    shuffled = np.random.permutation(all_numbers)
    return shuffled[:desired_number]

def save_random_frame(cap, frame_number, image_name, image_filter, autocropper):
                
    # Sets the image to be read to the randomly selected frame
    cap.set(1, frame_number)
    
    ret, frame = cap.read()
    
    # Checks to see if cap can even be retrieved
    if not ret:
        return
    
    frame = process_frame(frame, image_filter, autocropper)
        
    # Saves image of the current frame in jpg file
    print ('Creating...' + image_name)   
    cv2.imwrite(image_name, frame)
    
if __name__ == '__main__':
    main()
