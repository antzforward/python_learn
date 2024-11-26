p=(4,5)
x,y=p
print(x,y)
data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, date = data
print(name)
print(date)

name, shares, price, (year, mon, day) = data
print(name)
print(year)
print(day)

'''
name, shares, price, (year, mon) = data
由于数量不匹配，有没有声明解析任意数量的情况，会报错。
'''



s = 'Hello'
a, b, c, d, e = s
print(a,b,e,end='\n')

data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
_, shares, price, _ = data
print(shares,price,end='\n')