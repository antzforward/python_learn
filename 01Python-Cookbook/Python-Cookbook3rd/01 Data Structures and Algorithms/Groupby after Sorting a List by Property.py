"""
这里是在sorted 之后然后调用groupby
把对应属性接近的排成了group（底层用List来存储）
"""

rows = [
 {'address': '5412 N CLARK', 'date': '07/01/2012'},
 {'address': '5148 N CLARK', 'date': '07/04/2012'},
 {'address': '5800 E 58TH', 'date': '07/02/2012'},
 {'address': '2122 N CLARK', 'date': '07/03/2012'},
 {'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
 {'address': '1060 W ADDISON', 'date': '07/02/2012'},
 {'address': '4801 N BROADWAY', 'date': '07/01/2012'},
 {'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
]

from operator import itemgetter
from itertools import groupby

sorted_rows = sorted( rows, key=itemgetter('date')) #同上面的Sorting a List by Property一样
# Iterate in groups
for date, items in groupby(sorted_rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print(' ', i)

# 当然可以用defaultdict 对应Mapping Keys to Multiple Values in a Dictionary.py
from collections import  defaultdict
rows_by_date = defaultdict(list)
for row in rows: #注意这个并不需要排序
    rows_by_date[row['date']].append( row )

print('*'*20)

for date,items in rows_by_date.items():
    print(date)
    for i in items:
        print(' ', i)