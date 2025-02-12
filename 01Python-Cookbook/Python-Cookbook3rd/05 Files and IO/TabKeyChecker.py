import csv
import sys
from collections import defaultdict
import os
import pathlib
import subprocess
import re

def check_tab_file(filename):
    # 读取前四行
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')

        # 读取表头
        headers = [next(reader) for _ in range(4)]

        # 获取PKEY位置
        pkey_columns = [i for i, val in enumerate(headers[1]) if val.startswith('PKEY')]

        if not pkey_columns:
            print(f"{filename}: 错误：未找到PKEY定义")
            return False

        # 创建字典记录行号
        key_dict = defaultdict(list)
        duplicates_found = False

        # 从第五行开始检查
        for line_num, row in enumerate(reader, start=5):
            if len(row) < max(pkey_columns) + 1:
                print(f"行 {line_num} 列数不足")
                continue

            # 生成组合Key
            key = tuple(row[i] for i in pkey_columns)

            # 检查Key有效性
            if any(not k.strip() for k in key):
                print(f"{filename}: 行 {line_num} 包含空Key值")
                continue

            # 记录重复情况
            if key in key_dict:
                duplicates_found = True
                key_dict[key].append(line_num)
            else:
                key_dict[key] = [line_num]

        # 输出重复结果
        if duplicates_found:
            print(f"{filename}:发现重复Key：{{")
            for key, lines in key_dict.items():
                if len(lines) > 1:
                    key_str = ' + '.join(key)
                    print(f"\tKey '{key_str}' 重复出现在行：{', '.join(map(str, lines))}")
            print(f"}}")
            return False
        else:
            print(f"{filename}:所有Key值唯一")
            return True

def main():
    files_dict = {}
    pattern = r'\.tab$'
    # fd -a -t d ^[0-9]+
    out_text = subprocess.check_output(['fd','-a','-t','f',pattern]).decode('utf-8')
    file_list = ( pathlib.Path(f) for f in out_text.split('\n') if f !='' )
    for filename in file_list:
        check_tab_file( filename )



if __name__ == "__main__":
    main()