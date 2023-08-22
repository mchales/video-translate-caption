# use the command pytube "playlist url" to download the videos

#then you can rename them with this code

import os

# specify the directory you want to rename files in
directory = './downloading/downloads'  # replace with your directory

files = os.listdir(directory)
print("here")
for i, file in enumerate(files, start=1):
    if file.endswith('.mp4'):  # check if the file is a mp4 file
        old_filepath = os.path.join(directory, file)
        new_filename = f'p1e{i}.mp4'
        new_filepath = os.path.join(directory, new_filename)
        os.rename(old_filepath, new_filepath)