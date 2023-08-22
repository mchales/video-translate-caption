from cnocr import CnOcr
import time
import os
from pypinyin import pinyin
from googletrans import Translator
import csv
import re
import shutil

def translate(video_file):
    """
    Translate Chinese text extracted from frames of a video.

    Args:
    - video_file (str): Path to the input video file.

    Procedure:
    1. Determines the name of the folder containing frames and the associated CSV file based on the video's filename.
    2. Initializes the Chinese OCR tool and the Google translator.
    3. Iterates through each frame image in the designated folder.
    4. Uses OCR to extract Chinese text from the image.
    5. Transforms the extracted text to its Pinyin representation.
    6. Translates the Chinese text to English. If translation fails, it retries up to 5 times.
    7. Saves the Chinese text, its Pinyin, and its English translation to the CSV file.
    8. If the Chinese text in a frame matches the text in the previous frame, reuses the Pinyin and translation from the previous frame.
    9. After processing all frames, the directory containing the frames is deleted.
    10. Outputs statistics on the number of characters attempted for translation and the actual number of characters translated.
    """
    # Extract filename without extension
    base_name = os.path.basename(video_file)
    file_name = os.path.splitext(base_name)[0]

    # Corresponding frames directory and CSV file for the video
    dir_path = f'./frames/frames_{file_name}'
    csv_path = f'./translations/translations_{file_name}.csv'

    ocr = CnOcr() 
    translator = Translator()

    prev_chinese_text = None
    prev_out_pinyin = None
    prev_translation = None
    num_chars_translated1 = 0
    num_chars_translated2 = 0
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Chinese', 'Pinyin', 'Translation'])  # Write header
        
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
                chinese_text = ' '.join(text_values)

                pattern = re.compile(r'[^\u4e00-\u9fa5。0-9]') 
                chinese_text = re.sub(pattern, '', chinese_text)
                
                if chinese_text != prev_chinese_text and chinese_text != "":
                    num_chars_translated2 += len(chinese_text)
                    list_of_lists = pinyin(chinese_text)
                    # Getting the pinyin of the text
                    out_pinyin = ' '.join(word[0] for word in list_of_lists)
                    # # Getting the translation of the text
                    for _ in range(5):  # Retry up to 5 times
                        try:
                            print(str(count) + ": " + chinese_text)
                            num_chars_translated1 += len(chinese_text)
                            translation = translator.translate(chinese_text, dest='en').text
                            print(str(count) + ": " + translation)
                            break
                        except Exception as e:
                            print(f"Translation failed with error {str(e)}. Retrying in 1 seconds...")
                            time.sleep(1)  # Wait for 1 seconds before retrying
                        
                    else:
                        print("Translation failed after 5 attempts.")
                        translation = ""
                    # Store the current translations for use in next iteration
                    prev_chinese_text = chinese_text
                    prev_out_pinyin = out_pinyin
                    prev_translation = translation
                else:
                    # Super strange bug that happened 1/10000 times where the chinese_text is empty but the other two are not
                    if chinese_text == "":
                        out_pinyin = ""
                        translation = ""
                    # If the text is the same as previous, use the stored values
                    out_pinyin = prev_out_pinyin
                    translation = prev_translation

                # Write to CSV
                writer.writerow([chinese_text, out_pinyin, translation])
            else:
                writer.writerow(["", "", ""])
            
            count += 1
    if os.path.exists(dir_path):
    # Attempt to remove the directory and its contents
        try:
            shutil.rmtree(dir_path)
        except Exception as e:
            print(f'Error while deleting directory {dir_path}: {str(e)}')
    else:
        print(f'The directory {dir_path} does not exist')
    
    print("Attempted to Translate " + str(num_chars_translated1) + " characters")
    print("Translated " + str(num_chars_translated2) + " characters")