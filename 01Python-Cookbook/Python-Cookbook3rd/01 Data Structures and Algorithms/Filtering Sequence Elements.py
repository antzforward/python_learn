'''
对应LINQ的filter
'''
"""
var mylist = [1, 4, -5, 10, -7, 2, 3, -1];
var query = from n in mylist
            where n>0
            select n;
query.Dump();
"""
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
n = [n for n in mylist if n>0] # myList.Where( n>0)
print( n )

"""
var names = new[] { "Tom", "Dick", "Harry", "Mary", "Jay" }.AsQueryable();

var query =
	from n in names
	where n.Length > 3
	let u = n.ToUpper()
	where u.EndsWith ("Y")
	select u;
	
query.Dump();
"""
names = ["Tom", "Dick", "Harry", "Mary", "Jay"]
n = [ u for n in names if len(n)>3 and (u:= n.upper()).endswith('Y')] # u:=n.upper()是一个let语句
print(n)
"""
string[] names = { "Tom", "Dick", "Harry", "Mary", "Jay" };
names.Where ((n, i) => i % 2 == 0).Dump ("Skipping every second element");
"""
names = ["Tom", "Dick", "Harry", "Mary", "Jay"]
n = [n for i,n in enumerate(names) if i%2 == 0]
print("Skipping every second element")
print( n )

mylist = [1, 4, -5, 10, -7, 2, 3, -1]*2
n = (n for n in mylist if n>0)
print( list(n) )# 这里n是一个迭代器，但是LINQ默认都是迭代器 所以没啥特殊的。
n = filter( lambda x:x>0,mylist)
print( list(n) )# n是个filter object

"""
以下代码可以替换python
var query = 
    from n in mylist
    where n>0
    select math.sqrt(n);
"""
import math
n = [math.sqrt(n) for n in mylist if n > 0]
print( n )

"""
使用 if else语句的情况，在Linq里面用?:三元运算符来表示，不过这种方式在LINQ里面比较少见
List<int> myList = new List<int> { -1, 2, -3, 4, 5, -6 };
// 使用查询表达式
var result = from n in myList
    select n > 0 ? n : 0;
result.Dump()
"""
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
n = [n if n>0 else 0 for n in mylist]
print( n )

"""
The compress() function then picks out the items corresponding to True values.
跟numpy的代码很像的啊，但是这个示例 可以认为是中间产品.
我用C# 写成这样。
var addresses = new List<string> {
"5412 N CLARK",
"5148 N CLARK",
"5800 E 58TH",
"2122 N CLARK",
"5645 N RAVENSWOOD",
"1060 W ADDISON",
"4801 N BROADWAY",
"1039 W GRANVILLE"
};
var counts = new List<int> {0, 3, 10, 4, 1, 7, 6, 1};

var query = addresses.Where((n,i)=>counts[i]>5);
query.Dump();

"""
from itertools import compress
addresses = [
 '5412 N CLARK',
 '5148 N CLARK',
 '5800 E 58TH',
 '2122 N CLARK',
 '5645 N RAVENSWOOD',
 '1060 W ADDISON',
 '4801 N BROADWAY',
 '1039 W GRANVILLE',
]
counts = [ 0, 3, 10, 4, 1, 7, 6, 1]

more5 = [n > 5 for n in counts]
print(list(compress(addresses, more5)))
# 使用filter函数过滤addresses
filtered_addresses = list(filter(lambda x: x[1], zip(addresses, more5)))# zip出现了tuple
print(filtered_addresses)
#根据上面的C# 的代码 似乎可以写成这样,答案相同。
more5 = [addr for i, addr in enumerate(addresses) if counts[i] > 5]
print( more5 ) #['5800 E 58TH', '1060 W ADDISON', '4801 N BROADWAY']
