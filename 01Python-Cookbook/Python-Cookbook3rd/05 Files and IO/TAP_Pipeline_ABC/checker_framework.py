import asyncio
import sys
import time
from pathlib import Path
from abc import ABC, abstractmethod
from collections import defaultdict



class CheckerBase(ABC):
    # 可配置参数
    SEMAPHORE_LIMIT = 50  # 并发控制
    ENCODING_RETRY = ['utf-8', 'utf-16', 'gb18030', 'ansi']  # 文件编码尝试顺序
    @abstractmethod
    async def check_file(self, file_path: Path, index: int) -> tuple[bool, str]:
        """需子类实现的具体检查逻辑"""
        pass
    @abstractmethod
    def file_pattern(self) -> str:
        """需子类定义的目标文件模式"""
        pass

    def error_formatter(self, raw_msg: str) -> str:
        """可选：统一错误信息格式化"""
        return raw_msg  # 默认直接返回原始信息

async def main_task(checker:CheckerBase, dir_name='.'):
    # 1. 准备阶段
    files = list(Path(dir_name).rglob(checker.file_pattern()))
    total = len(files)
    progress_queue = asyncio.Queue()

    # 2. 启动进度报告器（自动结束）
    reporter = asyncio.create_task(progress_reporter(checker,total, progress_queue))
    # 3. 执行核心任务
    semaphore = asyncio.Semaphore(checker.SEMAPHORE_LIMIT)

    async def worker(file_path, idx):
        async with semaphore:
            result = await checker.check_file(file_path, idx)
            await progress_queue.put((idx, result))

    # 使用固定线程池控制并发
    tasks = [
        asyncio.create_task(worker(f, i + 1))
        for i, f in enumerate(files)
    ]
    # 4. 等待完成并自动清理
    await asyncio.gather(*tasks)
    await progress_queue.put(None)  # 通知progress 结束
    await reporter


async def progress_reporter(checker:CheckerBase, total: int, queue: asyncio.Queue):
    processed = 0
    errors = []
    start_time = time.time()

    while processed < total:
        item = await queue.get()
        if item is None:
            print(f"\n处理完成，成功率: {processed}/{total}")
            break
        idx, (status, msg) = item
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
            errors.append((idx, checker.error_formatter(msg)))

    print(f"\n\n检测完成! 共发现 {len(errors)} 个异常")
    for idx, err in errors:
        print(f"#{idx}: {err}")