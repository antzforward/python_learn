from checker_framework import CheckerBase,main_task
import asyncio
import sys
from pathlib import Path
import re
import aiofiles
import yaml
from yaml import Loader, MappingNode
import traceback

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
class MatStencilChecker(CheckerBase):
    def file_pattern(self):
        return '*.mat'

    async def check_file(self, mat_path: Path, index: int):
        # 原check_tab_file逻辑移植至此
        encodes = super().ENCODING_RETRY
        for encoding in encodes:
            try:
                async with aiofiles.open(mat_path, mode='r', encoding=encoding ) as f:
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

                            floats_list = doc.get('Material', {}).get('m_SavedProperties', {}).get('m_Floats', [])

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
            except UnicodeError as e:  # UnicodeError or UnicodeEncodeError as e: 可以用or哦，但是他们有继承关系，选父类型即可
                if encodes.index(encoding) == len(encodes) - 1:
                    return False, str({"status": "error", "filename": mat_path, "message": f"不支持的格式: {str(e)}"})
            except Exception as e:
                return False, f"{mat_path} 解析失败: {''.join(traceback.format_exception(*sys.exc_info()))}"

import argparse
if __name__ == "__main__":
    # 创建 ArgumentParser 对象，并设置自定义的使用方法提示
    parser = argparse.ArgumentParser(
        usage="使用方法：python MatStencilChecker2.py <目标目录>",
        description="检查目标目录中的材质文件"
    )
    # 添加目标目录参数
    parser.add_argument("dir_path", type=str, help="Path to the directory")

    # 解析命令行参数
    args = parser.parse_args()

    # 检查目标目录是否存在
    target_folder = Path(args.dir_path)
    if not target_folder.is_dir():
        print(f"错误：{target_folder} 不是有效目录")
        sys.exit(1)

    # 初始化检查器并运行主任务
    checker = MatStencilChecker()  # 只需切换子类
    asyncio.run(main_task(checker,target_folder))