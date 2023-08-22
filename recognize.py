# This file is used for testing purposes

import re
from cnocr import CnOcr
import os
import cv2
import numpy as np

dir_path = './frames'
text = []
ocr = CnOcr() 

count = 0

while True:
    img_path = os.path.join(dir_path, f'frame{count}.jpg')
    if not os.path.isfile(img_path):
        break

    out = ocr.ocr(img_path)

    if out:
        text_values = []
        for item in out:
            text_values.append(item['text'])
        all_text = ' '.join(text_values)

        # Keep only Chinese characters, punctuation, and numbers
        pattern = re.compile(r'[^\u4e00-\u9fa5。0-9]') 
        all_text = re.sub(pattern, '', all_text)

        print(str(count) +  ": " + all_text)
        text.append(all_text)
    else:
        print(str(count) + ": No Text")
        text.append('')
    
    count += 1

print(text)
