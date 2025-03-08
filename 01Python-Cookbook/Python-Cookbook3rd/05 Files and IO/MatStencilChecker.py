## 这个程序是暴力的去检查所有的mat里面，如果包含了stencil 设置，并且是为了mask作用（不限于UI） 就检查是否是默认值
import re
import sys
import asyncio
import aiofiles
import yaml
import time
from yaml import Loader, MappingNode
from pathlib import Path

Stencil_Set = {
    "_Stencil": 0.0,
    "_StencilOp": 0.0,
    "_StencilComp": 8.0,
}


class UnityLoader(Loader):
    def __init__(self, stream):
        super().__init__(stream)
        self.add_multi_constructor('tag:unity3d.com,2011:', self.construct_unity_object)

    def construct_unity_object(self, loader, tag_suffix, node):
        """安全处理Unity对象锚点"""
        # 使用getattr避免属性不存在错误
        anchor = getattr(node, 'anchor', None)
        data = {
            '_unity_type': int(tag_suffix),
            '_unity_instance_id': int(anchor) if anchor else None
        }

        # 合并子节点内容
        if isinstance(node, MappingNode):
            mapping = self.construct_mapping(node)
            data.update(mapping)

        return data
async def check_mat_stencil(mat_path: Path,index:int) :
    try:
        async with aiofiles.open(mat_path, 'r', encoding='utf-8') as f:
            content = await f.read()

            # 关键修正：动态处理TAG定义
            cleaned = re.sub(
                r'^%YAML 1.1\s*\n',  # 匹配YAML版本声明
                '',
                content,
                flags=re.MULTILINE,
                count=1
            )
            cleaned = re.sub(
                r'^%TAG !u!.*?\n',  # 移除原有TAG行
                '',
                cleaned,
                flags=re.MULTILINE,
                count=1
            )

            # 确保每个文档继承TAG
            cleaned = re.sub(
                r'^---',
                '%TAG !u! tag:unity3d.com,2011:\n---',
                cleaned,
                flags=re.MULTILINE
            )

            # 流式解析
            docs = yaml.load_all(cleaned, Loader=UnityLoader)

            for doc in docs:
                # 筛选Material类型（_unity_type=21）
                if doc.get('_unity_type') == 21:

                    floats_list = doc.get('Material',{}).get('m_SavedProperties', {}).get('m_Floats', [])

                    floats = {}
                    if isinstance(floats_list, list):
                        for item in floats_list:
                            if isinstance(item, dict):
                                floats.update(item)
                    elif isinstance(floats_list, dict):
                        floats = floats_list
                    # 参数检查
                    for key, expected in Stencil_Set.items():
                        actual = floats.get(key)
                        if actual is not None and float(actual) != expected:
                            return False, f"{mat_path} 异常参数 {key}={actual}"
                    return True, ''
            return True, ''
    except Exception as e:
        return False, f"{mat_path} 解析失败: {str(e)}"


async def main_task(dir_name='.'):
    # 1. 准备阶段
    mat_files = list(Path(dir_name).rglob('*.mat'))
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
            result = await check_mat_stencil(file_path, idx)
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
        print("使用方法：python MatSencilChecker.py <目标目录>")
        sys.exit(1)
    folderpath = sys.argv[1]
    if not Path(folderpath).is_dir():
        print(f"错误：{folderpath} 不是有效目录")
        sys.exit(1)
    asyncio.run(main_task(folderpath))