from pypinyin import pinyin

list_of_lists = pinyin('地点就在美丽富饶的青青草原')
out_pinyin = ' '.join(word[0] for word in list_of_lists)

print(out_pinyin)