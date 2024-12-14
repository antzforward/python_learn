"""
Regex（Regular Expression 正则表达式） 常用来对字符串的模式进行解析，然后进行匹配。
对web的文本进行处理的比较多。
"""
import re

t = re.compile(r'[;,\s]\s*')
line = 'asdf   fjdk; afed, fjek,asdf, foo'
print( t.split( line ))#['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
s = re.compile(r'(;|,|\s)\s*') #()代表捕捉，在split之后，这些中间信息也会被捕捉到
print( s.split( line ))
print( s.split( line )[::2])#['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
# 用(?:)表示括号内部内容 不捕捉。
m = re.compile(r'(?:,|;|\s)\s*')
print(m.split( line )) #['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
line = '''The split() method of string objects is really meant for very simple cases, and does
not allow for multiple delimiters or account for possible whitespace around the delim‐
iters. In cases when you need a bit more flexibility, use the re.split() method:'''
print( m.split( line ))