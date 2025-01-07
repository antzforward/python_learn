"""
这是独立的处理方式，类似Everything的功能，名字匹配，ext：py
有几种方式：
1、os.walk
2、os.scandir
3、pathlib.Path
4、Path的glob方式：放弃，只是匹配方式不同
5、glob的glob方式：放弃，只是匹配差异
6、第三方的search/filter 工具，fd

一下写几个测试用例，用来检查文件夹或者文件名，开头以最多3个数字
如果满足要求的是dir，则遍历下面所有的文件
按照从上到下的匹配模式。
"""

from memory_profiler import profile
import time
import os
import re
from collections import  deque # BFS 模式要队列

root = "G:/" #根目录
headsRe = re.compile(r'^\d{2,3}[^.0-9]+$')
fileRe = re.compile(r'^\d{2,3}[^.]*\.[A-Za-z0-9]{2,}$') #只要有一个后缀 防止引用纯数字的表示文件名,这里从头开始，用match
PathPartRe = re.compile(r'\/\d{2,3}[^.0-9\/]+\/')#这里匹配字符串中间的部分，用search

os_walk_res = set()
@profile
def os_walk_all_root( top ):
    for root, dir, files in os.walk( top ,topdown=True):
        root = root.replace("\\", "/")+'/'
        if PathPartRe.search(root):
            for name in files:
                os_walk_res.add(root+name)
        else:
            for name in files:
                if fileRe.match( name ):
                    os_walk_res.add( root+name)

start_time = time.time()
os_walk_all_root(root)
print(f"os walk：耗时：{time.time() - start_time}秒") #os walk：耗时：11.790300607681274秒
print( len(os_walk_res) ) #5090

# 这里还是用os scandir，但是我用BFS的方式遍历这个过程
# 存储结果的列表或集合
os_walk_res3 = set()
@profile
def os_scandir_all_root_while(top ):
    queue = deque([(top,False)])  # BFS 方式
    while queue:  # 只要栈不为空，就继续处理
        current_dir,matched = queue.popleft()  # 弹出当前目录FIFO
        try:
            items = os.scandir(current_dir)
        except (PermissionError,FileNotFoundError,NotADirectoryError) as e:
            continue
        current_dir = current_dir + '/'
        for item in items:
            if item.is_file():
                if matched or fileRe.match(item.name):
                    os_walk_res3.add(f'{current_dir}{item.name}')
            elif item.is_dir() :
                childMatched = matched or headsRe.match(item.name)
                queue.append((item.path.replace('\\','/'),childMatched))  # 将子目录压入队列中，以便后续处理

start_time = time.time()
os_scandir_all_root_while(root)
print(f"os scan by BFS：耗时：{time.time() - start_time}秒") #os scan by BFS：耗时：12.280669689178467秒
print(len(os_walk_res3) ) #5092

# print(*(os_walk_res3 - os_walk_res), sep='\n')
# print('*-+'*20)
#
# print(*(os_walk_res - os_walk_res3), sep='\n')
# print('*-+'*20)


## pathlib 看着就先进一点啊
from pathlib import Path
os_walk_res4 = set()

@profile
def Path_iterdir_all_root_while(top):
    queue = deque([(Path(top), False)])  # 使用列表作为队列来存储待处理的目录
    while queue:  # 只要栈不为空，就继续处理
        current_dir, matched = queue.popleft()  # 弹出当前目录
        items = current_dir.iterdir()
        try:
            for item in items:
                if item.is_file():
                    if matched or fileRe.match(item.name):
                        os_walk_res4.add(str(item.resolve()))
                elif item.is_dir():
                    childMatched = matched or headsRe.match(item.name)
                    queue.append((item, childMatched))  # 将子目录加入队列中，以便后续处理
        except (PermissionError, FileNotFoundError, NotADirectoryError) as e:
            continue


start_time = time.time()
Path_iterdir_all_root_while(root)
print(f"path  iterdir by BFS：耗时：{time.time() - start_time}秒") #path  iterdir by BFS：耗时：29.120572805404663秒
print(len(os_walk_res4) ) #5092

# pathlib 可以说整体替换了os
os_walk_res5 = set()
@profile
def pathlib_walk_all_root( top ):
    for root, dir, files in Path.walk( Path(top) ,top_down=True):
        rootname  = str(root.resolve()).replace("\\", "/")+'/'
        if PathPartRe.search(rootname):
            for name in files:
                os_walk_res5.add(rootname+name)
        else:
            for name in files:
                if fileRe.match( name  ):
                    os_walk_res5.add( rootname+name)


start_time = time.time()
pathlib_walk_all_root(root)
print(f"pathlib walk：耗时：{time.time() - start_time}秒") #pathlib walk：耗时：15.977015733718872秒
print( len(os_walk_res5) ) #5092

#使用第三方工具fd，先找到所有满足要求的文件夹， 然后按照顺序把文件夹内部的文件添加进来
import subprocess
os_walk_res6 = set()
dir_re = re.compile(r'\\\d{2,3}[^.0-9\/]+\\')
fire_re= re.compile(r'\d{2,3}[^.]*\.[A-Za-z0-9]{2,}$')

@profile()
def fb_find_all_root( top ):
    out_text = subprocess.check_output(['fd','-a','-t','f',r'\d{2,3}[^.0-9\\]+',top]).decode('utf-8')
    files_list = [ f for f in out_text.split('\n') if f !='' ]
    for name in files_list:
        if dir_re.search(name):
            os_walk_res6.add(name)
        elif fire_re.search(name, name.rindex('\\')):
             os_walk_res6.add(name)

start_time = time.time()
fb_find_all_root(root)
print(f"fd walk：耗时：{time.time() - start_time}秒") #fd walk：耗时：1.0672664642333984秒
print( len(os_walk_res6) ) #6778



