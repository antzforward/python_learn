import csv
import time
from collections import defaultdict
import pathlib
import subprocess
import asyncio
import sys
import psutil

async def check_tab_file(filename,encode='utf-8'):
    '''
    异步处理单个文件
    :param filename:
    :return
    '''
    encodes = ['utf-8','utf-16','gb18030','ansi']
    index = encodes.index( encode )
    try:
        # 读取前四行
        with open(filename, 'r', encoding=encodes[index]) as f:
            reader = csv.reader(f, delimiter='\t')

            # 读取表头
            headers = [next(reader) for _ in range(4)]
            # 获取PKEY位置
            pkey_columns = [i for i, val in enumerate(headers[1]) if val.startswith('PKEY') or val == 'FUnique()']

            if not pkey_columns:
                return False,f"{filename}: 错误：未找到PKEY定义"

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
                return False,f"{filename}:{result_str}"
            else:
                return True,f"{filename}:所有Key值唯一"
    except UnicodeDecodeError as e:
        if index + 1 < len(encodes):
            return await check_tab_file(filename, encodes[index+1])
        else:
            return False, str({"status": "error", "filename": filename, "message": f"未知错误: {str(e)}"})
    except UnicodeError as e:
        if index + 1 < len(encodes):
            return await check_tab_file(filename, encodes[index+1])
        else:
            return False, str({"status": "error", "filename": filename, "message": f"未知错误: {str(e)}"})
    except Exception as e:
        return False,str({"status": "error", "filename": filename, "message": f"未知错误: {str(e),type(e)}"})

async def main(dir_name='.'):
    pattern = r'\.tab$'
    out_text = subprocess.check_output(['fd','-a','-t','f',pattern,dir_name]).decode('utf-8')
    file_list = ( pathlib.Path(f) for f in out_text.split('\n') if f !='' )
    tasks = [check_tab_file(filename ) for filename in file_list]
    results = await  asyncio.gather( * tasks )
    for result,log in results:
        print( log )
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法：python TabKeyCheck.py .")
        sys.exit(1)
    process = psutil.Process()
    # 获取内存信息
    mem_info = process.memory_info()
    print(f"Memory Usage: {mem_info.rss / 1024 ** 2:.2f} MB")  # RSS为常驻集大小
    start_time = time.time()
    asyncio.run(main(sys.argv[1]))
    end_time = time.time()
    # 计算并打印总耗时
    total_time = end_time - start_time
    print(f"总体消耗时间: {total_time} 秒")
    mem_info = process.memory_info()
    print(f"Memory Usage: {mem_info.rss / 1024 ** 2:.2f} MB")  # RSS为常驻集大小