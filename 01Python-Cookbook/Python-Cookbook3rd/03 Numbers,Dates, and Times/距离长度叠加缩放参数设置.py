def scale_segment_lengths(segment_lengths, total_length,total_scal = 0.5):
    num_segments = len(segment_lengths)
    segment_ratios = [length / total_length for length in segment_lengths]

    # 计算每个线段的缩放权重
    weights = [1 - ratio for ratio in segment_ratios]

    # 根据缩放权重和位置比例计算每个线段需要缩放的长度比例
    total_weight = sum(weights)
    scale_ratios = [total_scal * weight / ratio / total_weight for weight, ratio in zip(weights, segment_ratios)]

    return scale_ratios

# 示例调用
segment_lengths = [10, 15,39,15, 20,30]  # 每个线段的长度
total_length = sum(segment_lengths)  # 整体长线段的长度
scale_ratios = scale_segment_lengths(segment_lengths, total_length)
print(segment_lengths)
print(scale_ratios)