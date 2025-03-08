import csv
from collections import defaultdict
import sys
import asyncio
import time
from io import StringIO
import aiofiles
import psutil
from pathlib import Path
async def  check_tab_file( tab_path:Path, index :int):
    encodes = ['utf-8', 'utf-16', 'gb18030', 'ansi']
    for encoding  in encodes:
        try:
            # 读取前四行
            async with aiofiles.open(tab_path, 'r', encoding=encoding) as f:
                content = await f.read()
                content = StringIO(content)
                reader = csv.reader(content, delimiter='\t')

                # 读取表头
                headers = [next(reader) for _ in range(4)]
                # 获取PKEY位置
                pkey_columns = [i for i, val in enumerate(headers[1]) if val.startswith('PKEY') or val == 'FUnique()']

                if not pkey_columns:
                    return False,f"{tab_path}: 错误：未找到PKEY定义"

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
                    return False,f"{tab_path}:{result_str}"
                else:
                    return True,f"{tab_path}:所有Key值唯一"
        except UnicodeError as e: #UnicodeError or UnicodeEncodeError as e: 可以用or哦，但是他们有继承关系，选父类型即可
            if encodes.index( encoding ) == len(encodes) - 1:
                return False, str({"status": "error", "filename": tab_path, "message": f"未知错误: {str(e)}"})
        except Exception as e:
            return False,str({"status": "error", "filename": tab_path, "message": f"未知错误: {str(e),type(e)}"})
async def main_task(dir_name='.'):
    # 1. 准备阶段
    mat_files = list(Path(dir_name).rglob('*.Tab'))
    total = len(mat_files)
    progress_queue = asyncio.Queue()

    # 2. 启动进度报告器（自动结束）
    reporter = asyncio.create_task(
        progress_reporter(total, progress_queue)
    )

    # 3. 执行核心任务
    semaphore = asyncio.Semaphore(50)  # 固定并发数

    async def worker(file_path, idx):
        async with semaphore:
            result = await check_tab_file(file_path, idx)
            await progress_queue.put((idx, result))

    # 使用固定线程池控制并发
    tasks = [
        asyncio.create_task(worker(f, i + 1))
        for i, f in enumerate(mat_files)
    ]

    # 4. 等待完成并自动清理
    await asyncio.gather(*tasks)
    await progress_queue.put(None)  # 结束信号
    await reporter


async def progress_reporter(total: int, queue: asyncio.Queue):
    """实时进度显示器"""
    processed = 0
    errors = []
    start_time = time.time()

    while processed < total:
        item = await queue.get()
        if item is None:
            print(f"\n处理完成，成功率: {processed}/{total}")
            break
        idx, (status,msg) = item
        processed += 1

        # 计算实时速度
        elapsed = time.time() - start_time
        speed = processed / elapsed if elapsed > 0 else 0

        # 动态进度条
        progress = processed / total * 100
        sys.stdout.write(
            f"\r[{'#' * int(progress // 2):<50}] {progress:.1f}% | 已处理: {processed}/{total} | 速度: {speed:.1f} 文件/秒 | 最近状态：{'OK' if status else msg[:30]}")
        sys.stdout.flush()

        if not status:
            errors.append((idx, msg))

    # 最终报告
    print(f"\n\n检测完成! 共发现 {len(errors)} 个异常文件")
    for idx, err in errors:
        print(f"#{idx}: {err}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法：python TabKeyChecker.py <目标目录>")
        sys.exit(1)
    folderpath = sys.argv[1]
    if not Path(folderpath).is_dir():
        print(f"错误：{folderpath} 不是有效目录")
        sys.exit(1)
    asyncio.run(main_task(folderpath))
