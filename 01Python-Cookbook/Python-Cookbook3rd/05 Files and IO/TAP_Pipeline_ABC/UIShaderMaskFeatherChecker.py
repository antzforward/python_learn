from checker_framework import CheckerBase,main_task
from pathlib import Path
import asyncio
import sys
import aiofiles
from io import StringIO
import csv
import itertools
from collections import defaultdict
import traceback
class ShaderFeatherChecker(CheckerBase):
    def file_pattern(self):
        return '*.shader'

    async def check_file(self, tab_path: Path, index: int):
        # 原check_tab_file逻辑移植至此
        encodes = super().ENCODING_RETRY
        for encoding in encodes:
            try:
                # 读取前四行
                async with aiofiles.open(tab_path, 'r', encoding=encoding) as f:
                    content = await f.read()
                    content = StringIO(content)
                    reader = csv.reader(content, delimiter='\t')

                    # 读取表头
                    headers = list(itertools.islice(reader, 4))
                    # 获取PKEY位置
                    pkey_columns = [i for i, val in enumerate(headers[1]) if
                                    val.startswith('PKEY') or val == 'FUnique()']

                    if not pkey_columns:
                        return False, f"{tab_path}: 错误：未找到PKEY定义"

                    # 创建字典记录行号
                    key_dict = defaultdict(list)
                    duplicates_found = False

                    results = []
                    # 从第五行开始检查
                    for line_num, row in enumerate(reader, start=5):
                        if len(row) < max(pkey_columns) + 1:
                            results.append(f"行 {line_num} 列数不足")
                            continue

                        # 生成组合Key
                        key = tuple(row[i] for i in pkey_columns)

                        # 检查Key有效性
                        if any(not k.strip() for k in key):
                            results.append(f"行 {line_num} 包含空Key值")
                            continue

                        # 记录重复情况
                        if key in key_dict:
                            duplicates_found = True
                            key_dict[key].append(line_num)
                        else:
                            key_dict[key] = [line_num]

                    # 输出重复结果
                    if duplicates_found:
                        results.append(f"发现重复Key：{{")
                        for key, lines in key_dict.items():
                            if len(lines) > 1:
                                key_str = ' + '.join(key)
                                results.append(f"\tKey '{key_str}' 重复出现在行：{', '.join(map(str, lines))}")
                        results.append(f"}}")
                    if len(results) != 0:
                        result_str = "\n".join(results)  # 先创建带换行的结果字符串
                        return False, f"{tab_path}:{result_str}"
                    else:
                        return True, f"{tab_path}:所有Key值唯一"
            except UnicodeError as e:  # UnicodeError or UnicodeEncodeError as e: 可以用or哦，但是他们有继承关系，选父类型即可
                if encodes.index(encoding) == len(encodes) - 1:
                    return False, str({"status": "error", "filename": tab_path, "message": f"未知错误: {str(e)}"})
            except Exception as e:
                return False, f"{tab_path} 解析失败: {''.join(traceback.format_exception(*sys.exc_info()))}"

    def error_formatter(self, raw_msg):
        return f"[UIShader格式错误] {raw_msg}"  # 自定义错误前缀


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法：python UIShaderMaskFeatherChecker.py <目标目录>")
        sys.exit(1)
    target_folder = sys.argv[1]
    if not Path(target_folder).is_dir():
        print(f"错误：{target_folder} 不是有效目录")
        sys.exit(1)
    checker = ShaderFeatherChecker()  # 只需切换子类
    asyncio.run(main_task(checker,target_folder))