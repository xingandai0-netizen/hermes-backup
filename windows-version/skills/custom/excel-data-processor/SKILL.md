---
name: excel-data-processor
description: >-
  自动化Excel数据处理技能，支持数据清洗、转换、分析和可视化。
  当用户需要处理Excel文件时自动激活。
version: 1.0.0
author: Hermes Agent
activation: /excel-data-processor
metadata:
  created: 2026-04-17
  last_reviewed: 2026-04-17
  review_interval_days: 30
capabilities:
  - 读取Excel文件（.xlsx, .xls）
  - 数据清洗和标准化
  - 统计分析
  - 生成报告
  - 数据可视化
platforms:
  - hermes
  - claude-code
  - cursor
---

# /excel-data-processor

自动化Excel数据处理技能。

## 触发条件

当用户提到以下内容时激活：
- "处理Excel文件"
- "数据分析"
- "表格处理"
- "Excel报告"
- "数据清洗"

## 功能列表

1. **文件读取**
   - 支持.xlsx和.xls格式
   - 自动检测工作表
   - 处理大文件（分块读取）

2. **数据清洗**
   - 处理缺失值
   - 去除重复行
   - 数据类型转换
   - 异常值处理

3. **统计分析**
   - 基础统计（均值、中位数、标准差）
   - 相关性分析
   - 频率分布
   - 趋势分析

4. **报告生成**
   - 自动格式化报告
   - 图表生成
   - 导出为PDF/HTML

## 使用方法

```python
# 导入技能
from excel_data_processor import ExcelProcessor

# 初始化处理器
processor = ExcelProcessor()

# 读取Excel文件
data = processor.read_excel("sales_data.xlsx")

# 数据清洗
clean_data = processor.clean_data(data)

# 统计分析
stats = processor.analyze(clean_data)

# 生成报告
processor.generate_report(stats, "report.pdf")
```

## 命令行使用

```bash
# 处理单个文件
/excel-data-processor process data.xlsx --output report.pdf

# 批量处理
/excel-data-processor batch --input-dir ./data --output-dir ./reports

# 生成模板
/excel-data-processor template --type sales
```

## 配置选项

```yaml
# config.yaml
processing:
  chunk_size: 10000
  encoding: utf-8
  na_values: ["", "N/A", "null"]

output:
  format: pdf
  template: standard
  include_charts: true

analysis:
  confidence_level: 0.95
  outlier_method: iqr
```

## 依赖包

```
pandas>=2.0.0
openpyxl>=3.1.0
matplotlib>=3.7.0
seaborn>=0.12.0
jinja2>=3.1.0
```

## 错误处理

```python
try:
    processor.process("large_file.xlsx")
except FileTooLargeError:
    # 自动切换到分块模式
    processor.process_chunked("large_file.xlsx")
except DataFormatError as e:
    # 提供修复建议
    print(f"数据格式错误: {e}")
    print("建议: 检查表头是否正确")
```
