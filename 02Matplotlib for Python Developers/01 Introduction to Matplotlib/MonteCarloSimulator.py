import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import defaultdict


class MarkovChainSimulator:
    def __init__(self, transition_matrix):
        """
        输入参数：
        transition_matrix: 二维列表或numpy数组，形状(n_states, n_states)
        """
        self.transition_matrix = np.asarray(transition_matrix)
        self.n_states = self.transition_matrix.shape[0]
        self._validate_matrix()

    def _validate_matrix(self):
        """概率矩阵校验"""
        if not np.allclose(self.transition_matrix.sum(axis=1), 1):
            raise ValueError("每行概率之和必须为1")
        if (self.transition_matrix < 0).any():
            raise ValueError("概率值不能为负")

    def simulate(self, n_steps=100, initial_state=0):
        """
        模拟状态转移过程
        返回：状态序列列表
        """
        current = initial_state
        history = [current]
        for _ in range(n_steps - 1):
            current = np.random.choice(
                self.n_states,
                p=self.transition_matrix[current]
            )
            history.append(current)
        return history

    def analyze(self, history):
        """统计结果分析"""
        stats = {
            'state_counts': defaultdict(int),
            'transition_counts': defaultdict(int),
            'max_consecutive': defaultdict(int)
        }

        current_consecutive = defaultdict(int)
        prev_state = None

        for i, state in enumerate(history):
            stats['state_counts'][state] += 1
            if prev_state is not None:
                stats['transition_counts'][(prev_state, state)] += 1
            if state == prev_state:
                current_consecutive[state] += 1
                if current_consecutive[state] > stats['max_consecutive'][state]:
                    stats['max_consecutive'][state] = current_consecutive[state]
            else:
                current_consecutive.clear()
            prev_state = state

        return stats
def visualize_simulation(history, state_names):
    plt.figure(figsize=(15, 6))

    # 状态分布饼图
    plt.subplot(1, 2, 1)
    counts = pd.Series(history).value_counts(normalize=True)
    plt.pie(counts, labels=[state_names[i] for i in counts.index], autopct='%1.1f%%')
    plt.title('State Distribution')

    # 状态转移热力图
    plt.subplot(1, 2, 2)
    trans_matrix = pd.crosstab(
        pd.Series(history[:-1]),
        pd.Series(history[1:]),
        normalize='index'
    )
    sns.heatmap(trans_matrix, annot=True, cmap='Blues')
    plt.title('Transition Heatmap')

    plt.tight_layout()
    plt.savefig('simulation_analysis.png')


if __name__ == "__main__":
    # 示例矩阵（Common → Rare → Epic → Legendary）
    tm = [
        [0.4, 0.3, 0.2, 0.1],  # Common
        [0.2, 0.4, 0.3, 0.1],  # Rare
        [0.1, 0.2, 0.5, 0.2],  # Epic
        [0.0, 0.1, 0.3, 0.6]  # Legendary
    ]

    simulator = MarkovChainSimulator(tm)
    history = simulator.simulate(n_steps=1000, initial_state=0)
    stats = simulator.analyze(history)

    print(f"传奇装备平均间隔步数: {1000 / stats['state_counts'][3]:.1f}")
    print(f"最长连续获得普通装备: {stats['max_consecutive'][0]}次")

    visualize_simulation(history, ['Common', 'Rare', 'Epic', 'Legendary'])
