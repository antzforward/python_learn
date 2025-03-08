## 这个程序是暴力的去检查所有的mat里面，如果包含了stencil 设置，并且是为了mask作用（不限于UI） 就检查是否是默认值
import re
import sys
import asyncio
import aiofiles
import yaml
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
async def check_mat_stencil(mat_path: Path) -> tuple[bool, str]:
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
                    floats_list = doc.get('m_SavedProperties', {}).get('m_Floats', [])
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
    import psutil
    import time
    import subprocess
    import pathlib
    process = psutil.Process()
    # 获取内存信息
    mem_info = process.memory_info()
    start_time = time.time()
    pattern = r'\.mat$'
    out_text = subprocess.check_output(['fd','-a','-t','f',pattern,dir_name]).decode('utf-8')
    file_list = ( pathlib.Path(f) for f in out_text.split('\n') if f !='' )
    tasks = [check_mat_stencil(filename) for filename in file_list]
    results = await asyncio.gather( * tasks )
    end_time = time.time()
    # 计算并打印总耗时
    total_time = end_time - start_time
    print( f"总体消耗时间: {total_time} 秒", f"使用了内存: {(process.memory_info().rss - mem_info.rss) / 1024 ** 2:.2f} MB")
    for result,log in results:
        if not result:
            print( log )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法：python MatSencilChecker.py <目标目录>")
        sys.exit(1)
    folderpath = sys.argv[1]
    if not Path(folderpath).is_dir():
        print(f"错误：{folderpath} 不是有效目录")
        sys.exit(1)
    asyncio.run(main_task(folderpath))