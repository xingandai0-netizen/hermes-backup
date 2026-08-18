# AI中国传统文化算命网站竞品调研

**日期**: 2026-07-06
**市场规模**: 1000亿+ RMB（中国算命/玄学），在线100-150亿，年增10%+

## 主要竞品

| 竞品 | 定价 | 技术栈 | 用户规模 | 独特卖点 |
|------|------|--------|---------|---------|
| 灵渊AI (lingyuan.ai) | ¥9.9/次, ¥39.9/月 | GPT大模型 | 10万+ | 综合平台 |
| DeepOracle (deeporacle.ai) | 免费概览+付费 | 专业算法+AI | - | 八字+星盘+塔罗 |
| 周易bot (zhouyi.bot) | 免费+积分 | 自研大模型 | - | 玄学大模型工具箱 |
| FateMaster.AI | 订阅制 | AI驱动 | - | 东方智慧解析 |
| 参天AI (cantian.ai) | 订阅制 | bazi-mcp(385⭐) | 100万+ | 全球化+多语言 |
| 天机爻 (tianjiyao.com) | 免费Wiki+付费 | Next.js+DeepSeek | - | 知识库162篇 |
| 查八字 (jiazimao.cn) | App内购 | 自研神经网络 | - | 2万字报告,1500年经典 |
| BaZiWei (ziwei.ike.ba) | 免费+高级 | 开源算法 | - | 离线计算,开源 |

## 开源技术栈

| 需求 | 推荐库 | Stars | 安装 |
|------|--------|-------|------|
| 紫微斗数(JS/TS) | SylarLong/iztro | 3,900 | npm install iztro |
| 紫微斗数(Python) | iztro-py | 11 | pip install iztro-py |
| 农历/八字底层 | 6tail/lunar-python | 622 | pip install lunar_python |
| 八字排盘(功能全) | china-testing/bazi | 1,400 | git clone |
| 周易六爻 | kentang2017/ichingshifa | 256 | pip install ichingshifa |
| AI Agent集成 | openai-iztro-agents | 新 | pip install |

## 核心代码

```python
# 八字排盘
from lunar_python import Lunar, EightChar
lunar = Lunar.fromYmdHms(1990, 5, 15, 8, 0, 0)
ec = lunar.getEightChar()
print(f"年柱:{ec.getMonth()} 日柱:{ec.getDay()} 时柱:{ec.getTime()}")

# 紫微斗数
from iztro_py import astro
chart = astro.by_solar('2000-8-16', 6, '男', language='zh-CN')

# 周易六爻
from ichingshifa import ichingshifa
iching = ichingshifa.Iching()
result = iching.qigua_now()
```

## 合规策略

1. 定位为"中国传统文化AI研究与学习平台"而非"算命"
2. 所有页面加"仅供参考"免责声明
3. 不做具体凶吉预测，侧重性格分析和趋势参考
4. 参考天机爻"理性客观"定位

## 用户画像

- 30岁以下占47%，女性52%
- 一二线城市白领，高学历
- 单次付费意愿100元内
- 核心需求：人生迷茫时心理安慰、日常运势、自我探索
