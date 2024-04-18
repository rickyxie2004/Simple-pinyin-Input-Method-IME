import json
from collections import Counter
import re
import os

# 读取纯文本文件（GBK编码）
def read_text_file(filename):
    data = []
    with open(filename, 'r', encoding='gbk') as file:
        for line in file:
            # 解析每行的JSON对象
            entry = json.loads(line)
            data.append(entry)
    return data

# 获取文本中的单个汉字出现的次数
def get_character_count_from_text(data):
    character_count = Counter()
    for entry in data:
        # 获取标题和正文
        title = entry.get('title', '')
        html = entry.get('html', '')
        # 组合标题和正文
        text = title + ' ' + html
        # 使用正则表达式提取中文字符
        chinese_characters = re.findall(r'[\u4e00-\u9fa5]', text)
        # 统计单个汉字出现的次数
        character_count.update(chinese_characters)
    return character_count

# 读取拼音-汉字对照表
def read_pinyin_table(filename):
    pinyin_dict = {}
    with open(filename, 'r', encoding='gbk') as file:
        for line in file:
            line = line.strip()
            if line:
                pinyin, characters = line.split(' ', 1)
                pinyin_dict[pinyin] = characters.split()
    return pinyin_dict

# 将单个汉字统计结果按拼音分类
def group_by_character_pinyin(character_count, pinyin_dict):
    grouped_result = {}
    for character, count in character_count.items():
        pinyin = find_pinyin(character, pinyin_dict)
        if pinyin:
            if pinyin not in grouped_result:
                grouped_result[pinyin] = {"words": [], "counts": []}
            grouped_result[pinyin]["words"].append(character)
            grouped_result[pinyin]["counts"].append(count)
    return grouped_result

# 根据汉字查找拼音
def find_pinyin(character, pinyin_dict):
    for pinyin, characters in pinyin_dict.items():
        if character in characters:
            return pinyin
    return None

# 指定存储结果的JSON文件名
output_json_file = '1_word.txt'

# 指定包含txt文件的文件夹路径
folder_path = './training_set'

# 获取文件夹中所有txt文件的路径
txt_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]

# 处理所有txt文件并统计单个汉字出现的次数
total_character_count = Counter()
for txt_file in txt_files:
    data = read_text_file(txt_file)
    character_count = get_character_count_from_text(data)
    total_character_count.update(character_count)

# 读取拼音-汉字对照表
pinyin_table_file = 'pinyin_table.txt'
pinyin_dict = read_pinyin_table(pinyin_table_file)

# 将单个汉字统计结果按拼音分类
grouped_result = group_by_character_pinyin(total_character_count, pinyin_dict)

# 将结果存储为JSON（使用UTF-8编码）
with open(output_json_file, 'w', encoding='utf-8') as file:
    json.dump(grouped_result, file, ensure_ascii=False, indent=4)
 
print("success!")