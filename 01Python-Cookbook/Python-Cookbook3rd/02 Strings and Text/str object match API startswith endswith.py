"""
这里介绍最直接的检查，判断str 匹配项的
startswith：str头部匹配，返回True，False
endswith：str 尾部匹配，返回True，False
"""

filename = 'spam.txt'
print( filename.startswith('spam'))
# 要想不区别大小写，就要讲filename 转换为大小写，然后再调用startswith 如下
print( filename.lower().startswith('spam'))
print( filename.lower().endswith(('.txt','.py')))
# 文件名相关的处理
import os
filenames = os.listdir('..')
heads = [f"{i:02}" for i in range(1,20)]
for filename in filenames:
    if filename.startswith( tuple(heads)):
        filename = os.path.realpath( os.path.join('..', filename))
        if os.path.isdir( filename ):
            print( filename )


# 用pathlib 简单多了
from pathlib import Path

# 获取当前文件夹的父目录路径
parent_dir = Path('..')

# 构建文件头匹配模式列表
heads = [f"{i:02}" for i in range(1, 20)]

# 遍历父目录中的所有项
for item in parent_dir.iterdir():
    # 检查该项是否以指定头部开头并且是一个目录
    if any(item.name.startswith(head) for head in heads) and item.is_dir():
        # 输出绝对路径
        print(item.resolve())

# 简化版本，直接在打印时过滤和处理
parent_dir = Path('..')
heads = [f"{i:02}" for i in range(1, 20)]
print(*[item.resolve() for item in parent_dir.iterdir() if any(item.name.startswith(head) for head in heads) and item.is_dir()], sep='\n')

'''
for name in filenames:
    if os.path.isdir( name) and name.startswith( tuple(heads)):
        for dirname in os.listdir( name ):
            if os.path.isdir( dirname ):
                for filename in os.listdir( dirname ):
                    if filename.endswith('.py'):
                        print( filename )
'''