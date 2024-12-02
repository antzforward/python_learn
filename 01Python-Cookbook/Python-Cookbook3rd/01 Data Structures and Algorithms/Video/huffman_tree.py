from manim import *
import heapq
from collections import Counter, namedtuple


# 定义一个节点类
class HuffmanNode:
    def __init__(self, frequency, character=None, left=None, right=None):
        self.frequency = frequency
        self.character = character
        self.left = left
        self.right = right
        self.position = None  # Manim中使用的位置变量

    def __lt__(self, other):
        return self.frequency < other.frequency


def create_huffman_tree(frequency):
    priority_queue = [HuffmanNode(freq, char) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(left.frequency + right.frequency, left=left, right=right)
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]


def visualize_huffman_tree(root, position=ORIGIN, level=1, spacing=3):
    nodes = VGroup()
    lines = VGroup()
    if root:
        # 对于非叶子节点使用'*'作为标识，对于叶子节点显示字符
        label_text = '*' if root.character is None else root.character
        root_node = Dot().move_to(position)
        char_text = Text(label_text, font_size=24).next_to(root_node, UP)
        freq_text = Text(str(root.frequency), color=BLUE, font_size=20).next_to(root_node, DOWN)
        node_group = VGroup(root_node, char_text, freq_text)
        nodes.add(node_group)

        # 根据左右节点存在与否绘制连接线并递归调用函数
        if root.left:
            left_position = position + LEFT * spacing / (level ** 1.5) + DOWN * 1
            left_line = Line(start=root_node.get_center(), end=left_position + UP * 0.5)
            lines.add(left_line)
            left_nodes, left_lines = visualize_huffman_tree(root.left, left_position, level + 1, spacing)
            nodes.add(left_nodes)
            lines.add(left_lines)

        if root.right:
            right_position = position + RIGHT * spacing / (level ** 1.5) + DOWN * 1
            right_line = Line(start=root_node.get_center(), end=right_position + UP * 0.5)
            lines.add(right_line)
            right_nodes, right_lines = visualize_huffman_tree(root.right, right_position, level + 1, spacing)
            nodes.add(right_nodes)
            lines.add(right_lines)

    return nodes, lines


class HuffmanEncodingScene(Scene):
    def construct(self):
        text = Text("Huffman Encoding").to_edge(UP)
        self.play(Write(text))
        self.wait(1)

        frequency = {'a': 45, 'b': 13, 'c': 12, 'd': 16, 'e': 9, 'f': 5}
        huffman_tree_root = create_huffman_tree(frequency)
        huffman_tree_vgroup, lines = visualize_huffman_tree(huffman_tree_root)

        self.play(Create(lines), run_time=2)
        self.play(Create(huffman_tree_vgroup), run_time=2)
        self.wait(2)


if __name__ == "__main__":
    scene = HuffmanEncodingScene()
    scene.render()