---
name: academic-research
description: "Academic research and paper writing. Search arXiv papers, write ML papers for top venues (NeurIPS/ICML/ICLR), literature review, and paper formatting. Use when user wants to search papers, write research papers, do literature review, or prepare academic submissions."
version: 1.0
tags: [arxiv, research, paper, academic, ml, neurips, icml, literature-review]
---

# Academic Research & Paper Writing

## arXiv Paper Search

### 搜索方式
```bash
# 按关键词
curl "http://export.arxiv.org/api/query?search_query=all:transformer&max_results=5"

# 按作者
curl "http://export.arxiv.org/api/query?search_query=au:vaswani&max_results=5"

# 按分类
curl "http://export.arxiv.org/api/query?search_query=cat:cs.CL&max_results=5"

# 按ID
curl "http://export.arxiv.org/api/query?id_list=2301.07041"
```

### 分类代码
- `cs.CL` — 计算语言学/NLP
- `cs.CV` — 计算机视觉
- `cs.LG` — 机器学习
- `cs.AI` — 人工智能
- `stat.ML` — 统计机器学习

## ML Paper Writing

### 论文结构（NeurIPS/ICML/ICLR标准）
1. **Abstract** — 问题+方法+结果（150-250词）
2. **Introduction** — 背景+动机+贡献列表
3. **Related Work** — 按主题分组，突出差异
4. **Method** — 模型架构+训练策略+理论分析
5. **Experiments** — 数据集+基线+消融实验
6. **Conclusion** — 总结+局限+未来工作

### 写作原则
- **清晰优先** — 不要为了显得"学术"而写复杂句子
- **数据说话** — 每个claim都要有实验支持
- **公平比较** — 基线方法要用最佳配置
- **可复现** — 提供代码链接和超参数

### 常见拒稿原因
1. 缺乏novelty（只是增量改进）
2. 实验不充分（缺少消融实验/错误分析）
3. 写作质量差（语法错误/逻辑不清）
4. 与已有工作重复

## LaTeX 模板

### NeurIPS
```latex
\documentclass{article}
\usepackage{neurips_2026}
\title{Paper Title}
\author{Author Name\\Affiliation}
\begin{document}
\maketitle
\begin{abstract}
...
\end{abstract}
\end{document}
```

## Consolidated From
| Former Skill | Content |
|---|---|
| `arxiv` | arXiv API search by keyword/author/category/ID |
| `research-paper-writing` | ML paper writing for NeurIPS/ICML/ICLR |
