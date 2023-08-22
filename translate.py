# This file is used for testing purposes

from googletrans import Translator
import time
# from google.cloud import translate_v2 as translate

# translate_client = translate.Client()

# translation = translate_client.translate("地点就在美丽富饶的青青草原", dest='en')
# print(translation['translatedText'])

try:
    translator = Translator()
    translation = translator.translate("地点就在美丽富饶的青青草原", dest='en')
    print(translation.text)

except Exception as e:
    print(f"An unexpected error occurred: {e}")

