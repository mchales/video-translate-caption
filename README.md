# Video Translation Project

This project automates the extraction of Chinese text from video frames, translates that text, and then adds the extracted text, its Pinyin, and the translation as subtitles to the video.v

The addition of Pinyin assists students in proper pronunciation and tones, bridging the gap between written characters and spoken language. Furthermore, by including a translation as subtitles, learners can immediately understand the meaning and context, fostering a holistic and immersive learning experience.

Demo: This is the first 20 seconds of [video](https://www.youtube.com/watch?v=ns4hTp7mdco&list=PLCxAtDkpA3f_s1q3rhRVEPnWX1o2utFk1).

![Alt Text for the GIF](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnFkM2oyZDJmdmxxbXkya3F6cHNqYWp5OWcwMzJhb25ra2g3cDhucCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ioj9acS6io2ynIA6Ub/giphy-downsized-large.gif))

## Features

1. **Frame Extraction** - Extracts frames from a video.
2. **Text Translation** - Uses Optical Character Recognition (OCR) machine learning model to detect Chinese text in the frames, translates the detected text to English using Google translate API, and also provides its Pinyin with a pinyin python module. It is not perfect, however its very useful for learning.
3. **Subtitling** - Adds the original Chinese text, its Pinyin, and the English translation as subtitles to the video.
4. **Video Management** - Exports an mp4 to the captioned-videos folder.


## File Overview

1. `main.py`: The main entry point for the application.
2. `videoimages.py`: Contains the function responsible for extracting frames from a video.
3. `processing.py`: Contains the function responsible for detecting Chinese text from the frames, translating it, getting the pinyin, and saving it in a CSV.
4. `addtovideo.py`: Add Chinese, Pinyin, and translation subtitles to a video.

## Parallel Processing

This project is optimized for performance by utilizing parallel processing capabilities. The system can simultaneously process multiple videos, dramatically reducing the time required to process a large batch of videos. I do batches 15 videos. With more videos there is a risk the Google Translate API will temporary block you. If the captions appear as empty caption blocks this is most likely the issue.


## Installation & Setup
1. Clone the repository to your machine:
2. Install the required Python packages:
3. Ensure ImageMagick is properly set up and the path is correctly configured in `caption.py`. You will need to download ImageMagick
4. (optional) Use the downloader to download an entire [playlist](https://www.youtube.com/playlist?list=PLCxAtDkpA3f8KxzGJKhv1AKaP5TEgvvyJ) and then run the `downloader.py` to rename files
5. Add video(s) to the videos folder.
6. Run the command
   ```python main.py```
7. Your output video is located in captioned-videos folder.
