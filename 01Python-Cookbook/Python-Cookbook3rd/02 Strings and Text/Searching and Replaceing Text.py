"""
有str自带的函数：
replace：查找并替换
re.sub: 使用正则表达式匹配的方式，然后替换，这个难度较大一点，但是更适合模式
"""
#replace

text = 'yeah, but no, but yeah, but no, but yeah'
#replace 产生新的str 对象，注意这里的replace等同于replace all，所有找到的都替换,限制数量 放在第三个参数上。
print( text.replace('yeah','yep') )#yep, but no, but yep, but no, but yep
print( text.replace('yeah','yep',1) )#yep, but no, but yep, but no, but yeah

text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
import re
# 第一个参数 匹配模式，第二个参数替换模式，第三个参数 content，
print( re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text) ) #Today is 2012-11-27. PyCon starts 2013-3-13.
# count 表示替换数量，默认全替换。
print( re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text ,count=1) )#Today is 2012-11-27. PyCon starts 3/13/2013.
# 当然正则表达式可以先编译，然后再匹配。
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
# r'\3-\1-\2' 不能编译吧，这个不是个合格的re表达式
print(datepat.sub(r'\3-\1-\2', text))#Today is 2012-11-27. PyCon starts 2013-3-13.
# repl 可以替换成 function的模式 以一定更复杂的情况,下面只是模拟 repl特殊的表达式，注意这个函数处理的是match对象
def change_date(m):
    return fr'{m.group(3)}-{m.group(1)}-{m.group(2)}'
print( datepat.sub( change_date,text)) #Today is 2012-11-27. PyCon starts 2013-3-13.
#sub，有个改进版本，subn，返回text，与匹配数量n
print((datepat.subn(change_date,text)) )

# str 常规的IGNORECASE，这里似乎只有拉丁语系才会这样,match时核心参数
text = 'UPPER PYTHON, lower python, Mixed Python'
print(re.findall('python', text, flags=re.IGNORECASE)) #['PYTHON', 'python', 'Python']
print( re.sub('python', 'snake', text, flags=re.IGNORECASE) ) # 'UPPER snake, lower snake, Mixed snake'

#最好是匹配到啥换啥，这时候用字定义函数来处理了
#这里是包装模式 delegate，通过内部函数闭包，讲内部函数跟传入参数word，
# 以及word处理产生的match对象的关系包装再matchcase这个函数内部了。
def matchcase(word):
     def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
     return replace

print(re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE))#'UPPER SNAKE, lower snake, Mixed Snake'

# 感觉每次都要做upper之类的操作，不合理，对比测试一下。
from memory_profiler import profile
import time
test_n  = 50000
# 测试第一种写法的性能和内存占用
start_time = time.time()
for i in range(test_n):
    re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE)
print(f"第一种写法耗时：{time.time() - start_time}秒")
# 使用memory_profiler测量内存占用
# profile装饰器可以测量函数级别的内存占用
@profile
def test_sequence_nocache():
    for i in range(test_n):
        re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE)
test_sequence_nocache()

cache={}
def matchcase_cached(word):
    # 预先计算word的各种形式
    if word not in cache:
        cache[word] = (
            word.upper(),
            word.lower(),
            word.capitalize()
        )
    word_upper, word_lower,word_capitalize= cache[word]

    def replace(m):
        text = m.group()
        if text.isupper():
            return word_upper
        elif text.islower():
            return word_lower
        elif text[0].isupper():
            return word_capitalize
        else:
            return word
    return replace
pattern = re.compile('python',flags=re.IGNORECASE)
start_time = time.time()
replace_func = matchcase_cached('snake')
for i in range(test_n):
    pattern.sub(replace_func, text )
print(f"第二种写法耗时：{time.time() - start_time}秒")
# 使用memory_profiler测量内存占用
# profile装饰器可以测量函数级别的内存占用
@profile
def test_sequence_cached():
    replace_func = matchcase_cached('snake')
    for i in range(test_n):
        pattern.sub( replace_func, text)
test_sequence_cached()

## 测试总结：
### 内存占用不多，并不一定是decorator节省，应该是字符串自身的cache效果
### 性能优化，主要题先在re.sub,还是compile之后用sub 提升比较少。