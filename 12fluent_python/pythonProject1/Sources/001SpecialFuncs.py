"""
每次都把这些内容写在script的首部，告诉自己我为什么要学习fluent python
首先，我希望写的代码越来越容易阅读，简单直接的可读性第一要务。
其次，这么久的python开发者，从我入行依赖，python伴我前进，它在upgrade，我不跟随我就degrade了。
最后，这本书真是太好，它可能会对我直接开发更广使用的库之类的代码，提供了框架级的指导，一定要多实践。实践才可能获得真知。
"""

## 下面用了namedtuple形式
import collections

#自动带来__str__ 以及访问属性的方式
Card = collections.namedtuple('Card',['rank','suit'])#字符串用单引号比较好
# 刚好凑成一张去掉大小王的扑克牌。52张
class FrenchDeck:
    # class attribute
    ranks = [str(n) for n in range(2,11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        # self 引用的的是Instance attribute
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

deck = FrenchDeck()
print( len(deck )) #52
print( deck[-1]) #Card(rank='A', suit='hearts')
from random import  choice
# 传入的seq 要满足支持__len__ 与__getitem__
print( choice(deck) )#Card(rank='6', suit='spades')
print( choice(deck) )#Card(rank='7', suit='clubs')
print( choice(deck) )#Card(rank='9', suit='spades')
#上面3个
print( deck[:3] )#[Card(rank='2', suit='spades'), Card(rank='3', suit='spades'), Card(rank='4', suit='spades')]
#每隔13，取一个，52%13=4
print( deck[12::13] )#[Card(rank='A', suit='spades'), Card(rank='A', suit='diamonds'), Card(rank='A', suit='clubs'), Card(rank='A', suit='hearts')]

for card in deck: # doctest: +ELLIPSIS
    print( card )

for card in reversed(deck): # doctest: +ELLIPSIS
    print( card )

print(  Card('Q', 'hearts') in deck  ) #True
print(  Card('7', 'beasts') in deck  ) #False
#建立一个map，对应key：value
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high( card ):
    rank_value = FrenchDeck.ranks.index( card.rank )
    # 牌号索引 2-A的index * 4 + 牌符号的index
    return rank_value * len( suit_values) + suit_values[card.suit]

print( spades_high(choice(deck)) )#6
print('log sorted card:')
# 完全类似的linq的写法了。
[print(card) for card in sorted(deck,key=spades_high)] #升序排列

## 下面是运算符号定义，Vector
from math import hypot
class Vector:
    def __init__(self, x=0, y=0):
        self.x,self.y = x,y
    # 目标是unambiguous ，无疑问
    def __repr__(self):
        return 'Vector(%r,%r)'%(self.x, self.y)

    def __abs__(self):
        return hypot( self.x, self.y)

    def __bool__(self):
        return bool(self.x  or  self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar )
    def __rmul__(self, scalar):
        return self.__mul__(scalar)


    ## repr 与 str的区别
    """
    repr:目标是明确的,但是可能会嵌套，用%r表示
    str：目标是可读，用%s
    容器 str 使用所包含的对象的repr,
    str的目标是可读性，在没有定义的情况下，用repr
    """
    def __str__(self):
        return 'Vector(%s,%s)'%(self.x, self.y)


# str的方式直接调用print 就可以了，然后能看到明显的转字符串了，repr 基本上保持了格式
print(Vector(1.2,3.4))
repr(Vector(5.6,7.8)) # 直接不打印在console里面了。
print('str :%s'%Vector(1.2,3.4))
print('repr :%r'%Vector(1.2,3.4))