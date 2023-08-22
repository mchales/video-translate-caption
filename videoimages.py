import cv2
import os, shutil
from constants import READ_RATE

def video_to_images(video_path):
    """
    Extract and save cropped frames from a given video at specified intervals.

    Args:
    - video_path (str): Path to the input video file.

    Procedure:
    1. Determines a unique output folder based on the video's filename.
    2. If the folder already exists, it clears any existing files.
    3. Opens the video and reads frames at regular intervals (defined by READ_RATE in seconds).
    4. Each read frame is cropped, taking roughly the bottom 1/6 of the frame 
       and removing 1/5 of the width from each side.
    5. The cropped frame is then saved to the designated folder.
    6. The process continues until the end of the video is reached.

    Note: Requires the `os`, `shutil`, and `cv2` modules to be imported.
    """

    # Extract filename without extension
    base_name = os.path.basename(video_path)
    file_name = os.path.splitext(base_name)[0]
    
    # Create a unique folder for each video file
    folder = f'./frames/frames_{file_name}'
    os.makedirs(folder, exist_ok=True)
    
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not video.isOpened():
        print("Error opening video")

    # Set the video frame rate
    fps = video.get(cv2.CAP_PROP_FPS)

    count = 0
    seconds = READ_RATE  # every READ_RATE seconds
    while True:
        video.set(cv2.CAP_PROP_POS_MSEC, seconds*1000)  # set the current time in milliseconds
        ret, frame = video.read()

        if not ret:
            break

        # Determine the bottom 1/6 part of the frame and cut 1/5 from either side
        height, width, layers = frame.shape
        start_row, start_col = int(height * 24/28), int(width * 1/5)  # Starting from approximately the bottom 1/6 of the image and 1/5 from the left side
        end_row, end_col = int(height * 27/28), int(width * 4/5)  # Ending at the bottom of the image and 1/5 from the right side
        cropped_frame = frame[start_row:end_row , start_col:end_col]

        # Save the frame as an image
        cv2.imwrite(os.path.join(folder, f"frame{count}.jpg"), cropped_frame)
        
        count += 1
        seconds += READ_RATE  # increment the current time by 0.5 seconds

    video.release()
    cv2.destroyAllWindows()
