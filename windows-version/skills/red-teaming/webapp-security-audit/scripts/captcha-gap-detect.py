#!/usr/bin/env python3
"""CAPTCHA滑块缺口位置检测
用法: python3 captcha-gap-detect.py <image_path>
输出: 缺口位置(x坐标)和建议的滑块拖动距离

依赖: pip install Pillow numpy
"""
import sys
from PIL import Image
import numpy as np

def find_gap(image_path):
    """分析CAPTCHA背景图，找到缺口位置"""
    img = Image.open(image_path)
    arr = np.array(img)
    height, width = arr.shape[:2]
    
    # 转灰度
    if len(arr.shape) == 3:
        gray = np.mean(arr, axis=2)
    else:
        gray = arr
    
    # 方法1: 亮度差异检测
    # 缺口区域通常比背景暗
    col_means = np.mean(gray, axis=0)
    window_size = 60  # 缺口通常40-80px宽
    min_mean = float('inf')
    gap_x = 0
    for x in range(width - window_size):
        window_mean = np.mean(col_means[x:x+window_size])
        if window_mean < min_mean:
            min_mean = window_mean
            gap_x = x
    
    # 方法2: 边缘检测
    # 缺口有强烈的垂直边缘
    gradient_x = np.abs(np.diff(gray, axis=1))
    edge_sum = np.sum(gradient_x, axis=0)
    
    # 找峰值
    mean_edge = np.mean(edge_sum)
    peaks = []
    for i in range(1, len(edge_sum)-1):
        if edge_sum[i] > edge_sum[i-1] and edge_sum[i] > edge_sum[i+1]:
            if edge_sum[i] > mean_edge * 1.5:
                peaks.append((i, float(edge_sum[i])))
    peaks.sort(key=lambda x: -x[1])
    
    # 方法3: 边缘对检测
    # 找间距40-80px的强边缘对(缺口左右边)
    gap_candidates = []
    for i in range(len(peaks)):
        for j in range(i+1, len(peaks)):
            dist = abs(peaks[j][0] - peaks[i][0])
            if 40 < dist < 80:
                left = min(peaks[i][0], peaks[j][0])
                right = max(peaks[i][0], peaks[j][0])
                center = (left + right) / 2
                gap_candidates.append({
                    'left': left, 'right': right,
                    'center': center, 'width': dist
                })
    gap_candidates.sort(key=lambda x: -x['width'])
    
    return {
        'image_size': (width, height),
        'brightness_method': gap_x,
        'edge_peaks': peaks[:10],
        'gap_candidates': gap_candidates[:5],
        'recommended_drag': gap_x
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 captcha-gap-detect.py <image_path>")
        sys.exit(1)
    
    result = find_gap(sys.argv[1])
    print(f"图片尺寸: {result['image_size']}")
    print(f"亮度法检测: 缺口在 x={result['brightness_method']}")
    print(f"边缘峰值: {result['edge_peaks'][:5]}")
    print(f"\n缺口候选:")
    for c in result['gap_candidates']:
        print(f"  左边={c['left']}, 右边={c['right']}, 中心={c['center']:.0f}, 宽度={c['width']}")
    print(f"\n建议拖动距离: ~{result['recommended_drag']}px")
