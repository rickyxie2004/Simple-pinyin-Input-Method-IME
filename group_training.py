import json
from collections import Counter
import re
# -*- coding:utf-8 -*-

import os

# 获取相邻两个字同时出现的次数
def get_adjacent_character_pairs(text):
    # 使用正则表达式提取中文字符，并去除空格
    chinese_characters = re.findall(r'[\u4e00-\u9fa5]', text.replace(' ', ''))
    # 构建相邻两个字的列表
    pairs = [chinese_characters[i] + ' ' + chinese_characters[i+1] for i in range(len(chinese_characters) - 1)]
    return pairs

# 读取纯文本文件（GBK编码）
def read_text_file(filename):
    data = []
    with open(filename, 'r', encoding='gbk') as file:
        for line in file:
            # 解析每行的JSON对象
            entry = json.loads(line)
            data.append(entry)
    return data

# 获取文本中的相邻两个字同时出现的次数
def get_adjacent_character_pairs_from_text(data):
    pairs_count = Counter()
    for entry in data:
        # 获取标题和正文
        title = entry.get('title', '')
        html = entry.get('html', '')
        # 组合标题和正文
        text = title + ' ' + html
        # 获取相邻两个字同时出现的次数
        pairs = get_adjacent_character_pairs(text)
        # 统计次数
        pairs_count.update(pairs)
    return pairs_count

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

# 将统计结果按照两个字的拼音分类
def group_by_character_pinyin(pairs_count, pinyin_dict):
    grouped_result = {}
    for pair, count in pairs_count.items():
        first_char, second_char = pair.split()
        first_pinyin = find_pinyin(first_char, pinyin_dict)
        second_pinyin = find_pinyin(second_char, pinyin_dict)
        if first_pinyin and second_pinyin:
            pinyin_key = first_pinyin + ' ' + second_pinyin
            if pinyin_key not in grouped_result:
                grouped_result[pinyin_key] = {"words": [], "counts": []}
            grouped_result[pinyin_key]["words"].append(pair)
            grouped_result[pinyin_key]["counts"].append(count)
    return grouped_result

# 根据汉字查找拼音
def find_pinyin(character, pinyin_dict):
    for pinyin, characters in pinyin_dict.items():
        if character in characters:
            return pinyin
    return None

# 指定存储结果的JSON文件名
output_json_file = '2_word.txt'

# 指定包含txt文件的文件夹路径
folder_path = './training_set'

# 获取文件夹中所有txt文件的路径
txt_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]

# 处理所有txt文件并统计相邻两个字同时出现的次数
total_pairs_count = Counter()
for txt_file in txt_files:
    data = read_text_file(txt_file)
    pairs_count = get_adjacent_character_pairs_from_text(data)
    total_pairs_count.update(pairs_count)

# 读取拼音-汉字对照表
pinyin_table_file = 'pinyin_table.txt'
pinyin_dict = read_pinyin_table(pinyin_table_file)

# 将统计结果按照两个字的拼音分类
grouped_result = group_by_character_pinyin(total_pairs_count, pinyin_dict)

# 将结果存储为JSON（使用UTF-8编码）
with open(output_json_file, 'w', encoding='utf-8') as file:
    json.dump(grouped_result, file, ensure_ascii=False, indent=4)
print("success!")
