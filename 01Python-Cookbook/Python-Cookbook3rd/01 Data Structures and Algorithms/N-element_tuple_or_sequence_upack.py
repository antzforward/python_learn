p=(4,5) # 这是个tuple
x,y=p
print(x,y)
data = ['ACME', 50, 91.1, (2012, 12, 21)]#这是sequence 形式,第四个是tuple
name, shares, price, date = data
print(name)
print(date)

name, shares, price, (year, mon, day) = data #解析成多个变量和一个tuple，同时tuple也解析了
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

a,*b,c = 'Hello'
print(a,c,end='\n')#H o

data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
_, shares, price, _ = data # _ 可以认为是不要的变量，占位的作用，变量数量还要匹配到数量
print(shares,price,end='\n') #50 91.1