import os
import glob
import multiprocessing

from videoimages import video_to_images
from processing import translate
from addtovideo import caption

def process_video(args):
    """
    Process a video by extracting images, translating the text present, adding subtitles, and then removing the original video.

    Args:
    - args (tuple): A tuple containing:
        1. video_file (str): Path to the input video file.
        2. output_file (str): Path where the processed video will be saved.

    Procedure:
    1. Extract frames (images) from the input video.
    2. Translate any Chinese text found in the frames to English.
    3. Add Chinese, Pinyin, and translated English subtitles to the video.
    4. Delete the original video file.

    Outputs:
    The function prints the current process and its progress using the process's unique ID (PID).
    """

    video_file, output_file = args
    print(f"Process {os.getpid()} starting to extract images from video...")
    video_to_images(video_file)

    print(f"Process {os.getpid()} starting to translate images...")
    translate(video_file)

    print(f"Process {os.getpid()} starting to add subtitles to video...")
    caption(video_file, output_file)

    print(f"Process {os.getpid()} deleting original video file: {video_file}...")
    os.remove(video_file)

if __name__ == "__main__":

    # Directory with videos to process
    videos_dir = 'videos'

    # Directory to save processed videos
    output_dir = 'captioned-videos'

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get list of all video files
    video_files = glob.glob(os.path.join(videos_dir, '*'))  # adjust the pattern inside as needed (e.g., '*.mp4')

    # Prepare list of arguments for each process
    process_args = []
    for video_file in video_files:
        output_file = os.path.join(output_dir, os.path.basename(video_file))
        process_args.append((video_file, output_file))

    # Create a pool of processes
    with multiprocessing.Pool() as pool:
        pool.map(process_video, process_args)