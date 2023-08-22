import csv
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
from constants import READ_RATE

def caption(video_file, output_path):
    """
    Add Chinese, Pinyin, and translation subtitles to a video.

    Args:
    - video_file (str): Path to the input video file.
    - output_path (str): Path where the captioned video will be saved.

    Procedure:
    1. Determines the name of the CSV file associated with the video. This file contains Chinese text, its corresponding
       Pinyin, and translation.
    2. Reads the CSV file and extracts subtitles at regular intervals (defined by READ_RATE in seconds).
    3. For each subtitle, it checks if the Pinyin and translation exist; otherwise, it uses "ERROR" as a placeholder.
    4. Places the Chinese text at the top, Pinyin at about 3/4 down, and the translation at the bottom of the video.
    5. Combines the original video and the subtitles.
    6. Outputs the result to the specified output path and removes the CSV file after processing.
    """
    # Extract filename without extension
    base_name = os.path.basename(video_file)
    file_name = os.path.splitext(base_name)[0]

    # Corresponding CSV file for the video
    csv_path = f'./translations/translations_{file_name}.csv'

    subs_chinese = []
    subs_pinyin = []
    subs_translation = []

    generator = lambda txt: TextClip(txt, font='Microsoft-YaHei-Bold-&-Microsoft-YaHei-UI-Bold', bg_color = "black", fontsize=24, color='white')

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        t = 0  # start time
        for row in reader:
            if row[0]:  # if Chinese text exists
                chinese, pinyin, translation = row
                if pinyin == '':  # if pinyin is empty
                    pinyin = 'ERROR'
                if translation == '':  # if translation is empty
                    translation = 'ERROR'
                subs_chinese.append(((t, t + READ_RATE), chinese))
                subs_pinyin.append(((t, t + READ_RATE), pinyin))
                subs_translation.append(((t, t + READ_RATE), translation))
            t += READ_RATE

    video = VideoFileClip(video_file)

    video_height = video.size[1]  # get the height of the video
    vertical_position = int(video_height * 0.82)  # calculate 3/4 of the video's height

    subtitles_chinese = SubtitlesClip(subs_chinese, generator).set_pos(('center','top'))
    subtitles_pinyin = SubtitlesClip(subs_pinyin, generator).set_pos(('center', vertical_position))
    subtitles_translation = SubtitlesClip(subs_translation, generator).set_pos(('center','bottom'))

    result = CompositeVideoClip([video, subtitles_chinese, subtitles_pinyin, subtitles_translation])
    result.write_videofile(output_path)
    os.remove(csv_path)