---
name: docx-annotation-extractor
description: 从Word文档(.docx)中提取批注(comments)和标红文本(red text)，识别用户任务指令并执行。适用于AI日报、论文、报告等文档的批注任务自动化。触发：读取批注、提取标红、docx批注、日报任务、批注任务、标红内容。
author: 小黑
created: 2026-04-30
tags: [docx, word, annotation, comment, red-text, task-extraction]
triggers:
  - 读取批注
  - 提取标红
  - docx批注
  - word批注
  - 日报任务
  - 批注任务
  - 标红内容
---

# DocX批注+标红提取与任务执行技能

从Word文档(.docx)中提取批注(comments)和标红文本(red text)，识别用户任务指令并执行。

## 使用场景
- 用户在AI日报Word文件中用批注标注任务（如"给出报告"、"接入XX"）
- 用户用红色字体标注重点内容
- 需要自动化读取批注→理解任务→执行→反馈

## 执行步骤

### Step 1: 提取批注(Comments)
```python
import zipfile
import xml.etree.ElementTree as ET

def extract_comments(docx_path):
    """从docx提取所有批注，返回 [{id, author, date, text, paragraph_refs}]"""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    results = []
    
    with zipfile.ZipFile(docx_path, 'r') as z:
        if 'word/comments.xml' not in z.namelist():
            return results
        
        tree = ET.parse(z.open('word/comments.xml'))
        comments = tree.getroot().findall('.//w:comment', ns)
        
        doc_tree = ET.parse(z.open('word/document.xml'))
        paras = doc_tree.getroot().findall('.//w:body/w:p', ns)
        
        comment_paras = {}
        for p_idx, p in enumerate(paras):
            for cr in p.findall('.//w:commentRangeStart', ns):
                cid = cr.get('{%s}id' % ns['w'], '')
                comment_paras.setdefault(cid, []).append(p_idx)
            for cr in p.findall('.//w:commentReference', ns):
                cid = cr.get('{%s}id' % ns['w'], '')
                comment_paras.setdefault(cid, []).append(p_idx)
        
        for c in comments:
            cid = c.get('{%s}id' % ns['w'], '')
            author = c.get('{%s}author' % ns['w'], 'unknown')
            date = c.get('{%s}date' % ns['w'], '')
            texts = c.findall('.//w:t', ns)
            content = ''.join([t.text or '' for t in texts])
            
            ref_texts = []
            for pid in comment_paras.get(cid, []):
                if pid < len(paras):
                    pt = ''.join([t.text or '' for t in paras[pid].findall('.//w:t', ns)])
                    if pt.strip():
                        ref_texts.append(pt)
            
            results.append({
                'id': cid,
                'author': author,
                'date': date,
                'text': content,
                'paragraph_context': ref_texts
            })
    
    return results
```

### Step 2: 提取标红文本(Red Text)
```python
def extract_red_text(docx_path):
    """从docx提取所有红色字体文本"""
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    red_colors = {'FF0000', 'RED', 'FF3333', 'CC0000', 'FF4444', 'C00000', 'FF5555'}
    results = []
    
    with zipfile.ZipFile(docx_path, 'r') as z:
        doc_tree = ET.parse(z.open('word/document.xml'))
        paras = doc_tree.getroot().findall('.//w:body/w:p', ns)
        
        for p_idx, p in enumerate(paras):
            red_parts = []
            full_text_parts = []
            
            for r in p.findall('.//w:r', ns):
                rt = r.find('w:t', ns)
                text = rt.text if rt is not None else ''
                full_text_parts.append(text or '')
                
                rpr = r.find('w:rPr', ns)
                if rpr is not None:
                    color = rpr.find('w:color', ns)
                    if color is not None:
                        val = color.get('{%s}val' % ns['w'], '').upper()
                        if val in red_colors and text:
                            red_parts.append(text)
            
            if red_parts:
                results.append({
                    'paragraph_index': p_idx,
                    'full_text': ''.join(full_text_parts),
                    'red_text': ''.join(red_parts)
                })
    
    return results
```

### Step 3: 识别任务指令
批注内容通常是任务指令，分类为：
- 任务指令（"给出报告"、"能否学习/接入"）
- 反馈意见（"写得好"、"需要修改"）
- 问题（"能否完成XX"）
- 观察项（"设入观察区"）

### Step 4: 执行任务
按优先级顺序执行，完成后在原文档旁生成结果文件。

### Step 5: 生成执行报告
输出格式见 Step 6 示例。

## 注意事项
- python-docx 不支持直接读取批注，必须用 zipfile+ET 解析XML
- 标红检测需覆盖多种红色值（FF0000, C00000, CC0000等）
- 批注ID与段落通过 commentRangeStart/commentRangeEnd/commentReference 关联
- 同一批注可能关联多个段落（开始段和引用段）
- 执行任务前先搜索session_search看是否已有相关产出

## 陷阱：创建docx ≠ 提取docx
- 本技能只负责**读取**批注和标红，不负责**创建**新 docx 文件
- 如果用户要求「写一篇论文并保存为 .docx」，这是**代码生成任务**→ 委托小白猪(Roo Code)
- 不要自己在终端/execute_code 里反复尝试 pip install python-docx（沙盒环境 pip 不可用）
- 小白猪可在 VS Code 终端执行：`uv venv && uv pip install python-docx`，然后运行脚本生成文档
