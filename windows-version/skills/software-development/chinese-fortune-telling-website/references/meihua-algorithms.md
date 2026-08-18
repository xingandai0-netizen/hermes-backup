# 梅花易数完整算法

## 先天八卦基础数据

```python
TRIGRAM_NAME = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤"}
TRIGRAM_WUXING = {"乾": "金", "兑": "金", "离": "火", "震": "木", "巽": "木", "坎": "水", "艮": "土", "坤": "土"}
TRIGRAM_XIANG = {"乾": "天", "兑": "泽", "离": "火", "震": "雷", "巽": "风", "坎": "水", "艮": "山", "坤": "地"}
```

## 时间起卦法

```python
def qigua_by_time(year_zhi_index, month, day, hour_zhi_index):
    """上卦=(年+月+日)%8, 下卦=(年+月+日+时)%8, 动爻=(年+月+日+时)%6"""
    def mod8(n): return n % 8 if n % 8 != 0 else 8
    def mod6(n): return n % 6 if n % 6 != 0 else 6
    
    total = year_zhi_index + month + day
    up = mod8(total)
    total += hour_zhi_index
    down = mod8(total)
    dong = mod6(total)
    return up, down, dong
```

## 数字起卦法

```python
def qigua_two_numbers(a, b):
    """上卦=a%8, 下卦=b%8, 动爻=(a+b)%6"""
    def mod8(n): return n % 8 if n % 8 != 0 else 8
    def mod6(n): return n % 6 if n % 6 != 0 else 6
    return mod8(a), mod8(b), mod6(a + b)

def qigua_three_numbers(a, b, c):
    """上卦=a%8, 下卦=b%8, 动爻=c%6"""
    def mod8(n): return n % 8 if n % 8 != 0 else 8
    def mod6(n): return n % 6 if n % 6 != 0 else 6
    return mod8(a), mod8(b), mod6(c)
```

## 本卦、互卦、变卦

```python
def get_hugua(up_yao, down_yao):
    """互卦：2,3,4爻为下卦，3,4,5爻为上卦"""
    all_yao = down_yao + up_yao  # 6爻，从下到上
    return all_yao[1:4], all_yao[2:5]

def get_biangua(up_yao, down_yao, dong_yao):
    """变卦：动爻阴阳反转"""
    all_yao = list(down_yao + up_yao)
    all_yao[dong_yao - 1] = 1 - all_yao[dong_yao - 1]
    return all_yao[:3], all_yao[3:]
```

## 变卦卦名查找
互卦和变卦必须显示完整卦名（如"火水未济"、"震为雷"），不能只显示上下卦名。
需要64卦完整数据表，key为`${上卦名}${下卦名}`，value含卦名、卦辞、诗词。

## 体用分析

```python
# 动爻所在卦为用卦，另一卦为体卦
# 五行生克关系：
# 用生体 = 大吉
# 体克用 = 吉
# 比和 = 平
# 体生用 = 凶
# 用克体 = 大凶
```
