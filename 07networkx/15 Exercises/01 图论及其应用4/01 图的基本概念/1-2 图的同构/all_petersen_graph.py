import networkx as nx
import inspect
import matplotlib.pyplot as plt
from networkx.drawing import layout

layout_func = {name: getattr(layout, name) for name in layout.__all__}


# 去掉参数中带n之类的需要设置的参数
def has_parameters(func, params):
    """Check if the function has the specified parameters."""
    sig = inspect.signature(func)
    return any(param in sig.parameters for param in params)


def _all_need_setting_params(func):
    """检查函数是否有指定的必需参数（无默认值的参数）"""
    sig = inspect.signature(func)
    # 获取所有没有默认值的必需参数
    required_params = [
        name for name, param in sig.parameters.items()
        if param.default is param.empty  # 没有默认值
           and param.kind not in (param.VAR_POSITIONAL, param.VAR_KEYWORD)  # 排除 *args 和 **kwargs
    ]
    return required_params

def has_func_name_keys(func, names ):
    """检查函数名字包含目标名字，比如planar"""
    # 获取函数名
    func_name = func.__name__
    func_keys = func_name.split('_')
    # 检查函数名是否包含names中的任意一个关键词
    return any(name.lower() in func_keys for name in names)

def has_required_parameters(func, params):
    required_params = _all_need_setting_params(func)
    # 检查所有必需参数是否都在params的键中
    return all( param in params for param in required_params )


# 必须包含的参数
needed_params = ['G']

# 不支持的类型 比如planar，这里我尽量不用try-catch 就是想找到哪些特点的不支持petersen
avoid_func_key =['planar','multipartite']

selected_layouts = {k: layout_func[k] for k in layout_func if
                    not has_func_name_keys(layout_func[k], avoid_func_key)
                    and has_required_parameters(layout_func[k], needed_params)}

# 创建和绘制图
rows = cols = int(len(selected_layouts) ** 0.5)
if rows * cols < len(selected_layouts): cols += 1
if rows * cols < len(selected_layouts): rows += 1

plt.figure(figsize=(cols * 4, rows * 4))

# 创建 Petersen 图
G = nx.petersen_graph()

for i, (name, layout) in enumerate(selected_layouts.items()):
    ax = plt.subplot(rows, cols, i + 1)
    # 处理函数参数
    pos = layout(G)
    nx.draw(G, pos, ax=ax, with_labels=True)
    ax.set_title(name)
    ax.set_aspect('equal')  # 这将使得 x 轴和 y 轴具有相同的比例

plt.tight_layout()
plt.savefig('all_petersen_graphs.png')
#plt.show()



## 用列出所有的layout函数的形式也行的,方便条参数
## 参数来源
import numpy as np
nodes = G.number_of_nodes();
k_value = 1/np.sqrt( nodes )
def scale_layout(layout_func):
    def scaled_layout(G, **kwargs):
        pos = layout_func(G, **kwargs)
        return pos
    return scaled_layout

# 定义一个字典来存储具有自定义参数的布局函数
compatible_layouts = {
    'circular_layout': lambda G: scale_layout(nx.circular_layout)(G),
    'fruchterman_reingold_layout': lambda G: scale_layout(nx.fruchterman_reingold_layout)(G, k=None ,seed=5, iterations=50),
    'kamada_kawai_layout': lambda G: scale_layout(nx.kamada_kawai_layout)(G, dist=None, pos=None, weight='weight'),
    'random_layout': lambda G: scale_layout(nx.random_layout)(G,seed=5),
    'shell_layout': lambda G: scale_layout(nx.shell_layout)(G, nlist=[range(5,10), range(5)]),
    'spring_layout': lambda G: scale_layout(nx.spring_layout)(G,seed=5, k=k_value*1.5, iterations=50),
    'spectral_layout': lambda G: scale_layout(nx.spectral_layout)(G,scale=1.5 ),
    #'planar_layout':lambda G:scale_layout(nx.planar_layout)(G), #平面不相交的图，不符合peterson graph的情况
    'spiral_layout':lambda G:scale_layout(nx.spiral_layout)(G),
    #'multipartite_layout':lambda G:scale_layout(nx.multipartite_layout)(G),
    'arf_layout':lambda G:scale_layout(nx.arf_layout)(G,pos=None),
}