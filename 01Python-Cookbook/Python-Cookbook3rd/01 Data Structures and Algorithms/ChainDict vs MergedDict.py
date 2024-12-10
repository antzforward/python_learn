"""
ChainMap 讲两个不同的Dict a，b 链接起来，a，b还有效，并且根据先后包留所有的数据
Merged：不是一个新类型，在dict上使用update方式更新，比如，a。update（b) b的内容赋值到a中，如update含义，相同key的值会变动。
ChainMap，它主要用于创建一个单一可视化的视图，该视图将多个字典组合在一起。使用 ChainMap 可以有效地管理和更新不同作用域或上下文中的属性。
以下是一些具体应用场景：
1.处理具有多个作用域的变量：如在编程环境中，你可能有局部变量和全局变量等多个命名空间。ChainMap 可以用来顺序查找这些不同作用域的变量。
2.参数默认值与用户设定值的合并：在函数调用时，经常需要处理默认参数和用户提供的参数。通过 ChainMap 可以先查找用户设置的参数值，如果没有设置，则回退到默认值。
3.实现继承链：在面向对象的环境中，可以使用 ChainMap 来模拟类（或对象）之间的继承关系，其中属性和方法的查找可以按照从子类到父类的顺序进行。
4.配置文件管理：当有多层配置文件时（比如系统级、用户级和项目级），ChainMap 可以用来组织这些配置文件，使得优先级高的设置会覆盖优先级低的设置。
5.上下文切换：ChainMap 可以非常便利地用于需要频繁更改上下文环境的情况，例如，在模拟器或线程执行环境的设置中。
使用 ChainMap 的优势在于无需真正合并字典，就能够在多个字典之间快速查找。这意味着内存使用和性能都可能优于简单地合并字典。
从上面的说明来看，ChainMap有很重要的工程含义。
我觉得可能在需要很多宏定义的shader编译流程中，非常好用吧 O(∩_∩)O
"""

from collections import ChainMap

defaults = {'theme': 'Default', 'language': 'Eng', 'show_errors': False}
user_settings = {'theme': 'Dark', 'show_errors': True}

# 创建ChainMap，优先使用user_settings中的设置
config = ChainMap(user_settings, defaults)

print(config['theme'])  # 输出: Dark
print(config['language'])  # 输出: Eng
print(config['show_errors'])  # 输出: True
## 优先级越高，放在前面。

a = {'x': 1, 'z': 3 }
b = {'y': 2, 'z': 4 }
c = ChainMap(a,b)
print(c['x']) # Outputs 1 (from a)
print(c['y']) # Outputs 2 (from b)
print(c['z']) # Outputs 3 (from a)

print( c ) #ChainMap({'x': 1, 'z': 3}, {'y': 2, 'z': 4})
print( c.parents ) #ChainMap({'y': 2, 'z': 4})
print( c.parents.parents ) #ChainMap({})
print( c.parents.items() ) #ItemsView(ChainMap({'y': 2, 'z': 4}))
print( c.maps ) # 从下面介绍，如果需要反复切换setting 的情况，就直接用maps的操作吧,这里返回的是个list

## 如果直接修改a，都会反映在c上面,反之亦然
a['x'] = 5
print(c,a) #ChainMap({'x': 5, 'z': 3}, {'y': 2, 'z': 4}) {'x': 5, 'z': 3}
c['x'] = 1
print(c,a)#ChainMap({'x': 1, 'z': 3}, {'y': 2, 'z': 4}) {'x': 1, 'z': 3}

## 下面表现常规意义的dict merged含义，用update的方式
merged = dict( b )
merged.update( a )
print( merged ) #{'y': 2, 'z': 3, 'x': 1} #不但数值变了，顺序也变了。x在后面，不过没关系
a['x'] = 5
print(merged,a) #{'y': 2, 'z': 3, 'x': 1} {'x': 5, 'z': 3} #彼此脱离了
merged['x'] = 4
print(merged,a) #{'y': 2, 'z': 3, 'x': 4} {'x': 5, 'z': 3} #彼此脱离了


## 用例1 local，global
from collections import ChainMap

def scope_test():
    local_scope = {'var': 'local'}
    global_scope = {'var': 'global', 'another_var': 'found'}

    env = ChainMap(local_scope, global_scope)

    # 优先查找 local_scope
    print(env['var'])  # 输出: local

    # 在 local_scope 找不到时，回退到 global_scope
    print(env['another_var'])  # 输出: found

scope_test()

## 用例2 设置合并，用户设置替代其他
from collections import ChainMap


def configure_app(user_settings=None):
    if user_settings is None:
        user_settings = {}

    default_settings = {'theme': 'Default', 'verbose': True}

    # 用户设置优先
    settings = ChainMap(user_settings, default_settings)
    print(settings)


configure_app({'theme': 'Dark', 'debug_mode': False})

## 实现继承链
from collections import ChainMap

class Parent:
    def __init__(self):
        self.attributes = {'name': 'Parent', 'items': [1, 2, 3]}

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.attributes = ChainMap({'name': 'Child'}, self.attributes)

    def get_attribute(self, key):
        return self.attributes[key]

child_instance = Child()
print(child_instance.get_attribute('name'))  # 输出: Child
print(child_instance.get_attribute('items'))  # 输出: [1, 2, 3]

## 配置文件管理
from collections import ChainMap

system_config = {'theme': 'Default', 'debug': False}
user_config = {'theme': 'Dark'}
project_config = {'debug': True}

config = ChainMap(project_config, user_config, system_config)
print(config['theme'])  # 输出: Dark
print(config['debug'])  # 输出: True

## 上下文切换
from collections import ChainMap

def context_manager(context_stack, new_context):
    context_stack.maps.insert(0, new_context)
    print(context_stack)

context_stack = ChainMap({'user': 'admin'})
print('Initial Context:', context_stack)  # 初始化上下文

# 切换到新的上下文环境
context_manager(context_stack, {'theme': 'Dark', 'user': 'guest'})

# 再次切换上下文
context_manager(context_stack, {'debug': True})

# 移除当前上下文
context_stack.maps.pop(0)
print('Back to Previous Context:', context_stack)

## 以上都是经典用法，还是要找一下具体的工程来对应的使用一下。
