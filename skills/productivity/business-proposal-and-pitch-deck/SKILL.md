---
name: business-proposal-and-pitch-deck
description: "Create investor pitch decks and business proposals (企划书/BP). Covers Sequoia/YC frameworks, SlideSage PPTX generation, officecli integration, and design best practices. Use when user asks for business plan, pitch deck, fundraising proposal, investor deck, 企划书, or 融资商业计划书."
version: 1.0
tags: [pitch-deck, business-proposal, slidesage, officecli, investor, fundraising]
---

# Business Proposal & Pitch Deck Creation

**触发条件**: 用户要求创建商业计划书、融资企划书、pitch deck、investor presentation

## 核心工作流

### 1. 研究阶段
- 收集公司/产品信息（产品描述、目标市场、商业模式、团队背景）
- 确定融资阶段（种子轮/A轮/B轮）和目标金额
- 确定输出格式（PPTX优先，HTML备选）

### 2. 内容框架（Sequoia/YC标准）
```
1. 封面 — 公司名+Logo+融资轮次+日期
2. 问题 — 痛点描述+市场规模
3. 解决方案 — 产品描述+核心价值
4. 产品展示 — 截图/Demo/工作流
5. 商业模式 — 收入来源+定价
6. 市场规模 — TAM/SAM/SOM
7. 竞争分析 — 竞品对比矩阵
9. 团队 — 核心成员+背景
10. 财务预测 — 3-5年收入预测
11. 融资需求 — 金额+用途+里程碑
12. 联系方式
```

### 3. 输出工具选择

#### SlideSage（推荐 — 非AI味PPTX）
```bash
# 安装
cd ~/slidesage && npm install

# 生成
node generate.js --input proposal.json --output deck.pptx
```
- 优点：叙事结构+设计品质，避免AI味
- 支持：自定义模板、品牌色、字体
- 输出：`.pptx` 格式

#### officecli（备选 — 文档操作）
```bash
# 创建PPTX
officecli create pptx --template business-plan

# 分析现有文档
officecli analyze document.docx
```
- 优点：支持docx/xlsx/pptx全格式
- 适用：修改现有文档、添加图表

#### HTML Slides（前端演示）
- 使用 `frontend-slides` 技能生成HTML格式
- 适用：在线分享、快速迭代

## 设计原则

### 避免AI味
- 不要过度使用渐变和阴影
- 不要堆砌emoji和图标
- 数据可视化要简洁专业
- 配色不超过3种主色
- 每页核心信息不超过3个

### 排版规范
- 标题：24-32pt，粗体
- 正文：14-18pt，常规
- 数据：用图表而非文字堆砌
- 留白：每页至少30%留白

## 常见陷阱

### 1. 信息过载
每页只讲一个核心观点，不要把所有信息塞进一页。

### 2. 缺少故事线
pitch deck是讲故事，不是罗列功能。要有清晰的叙事弧线。

### 3. 数据不一致
财务预测、市场规模、用户数据之间要逻辑自洽。

### 4. 忽略竞争分析
不要说"没有竞争对手"。要展示你理解市场格局。

## Consolidated From (archived skills)

| Former Skill | Unique Content |
|---|---|
| `business-proposal` | officecli集成、PPTX生成 |
| `business-proposal-creation` | SlideSage推荐、完整研究→设计→交付工作流 |
| `pitch-deck-creation` | Sequoia/YC框架、slide结构、内容收集方法 |
| `slidesage-pitch-deck` | SlideSage Node.js工具使用、非AI味PPTX生成 |
| `slidesage-pptx` | SlideSage PPTX生成（重复，已合并） |
