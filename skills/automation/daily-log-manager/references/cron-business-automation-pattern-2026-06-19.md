# Cron模式下运行业务自动化脚本的模式与降级方案

**日期**: 2026-06-19 (updated 2026-06-22)
**场景**: 自动化技术趋势收益系统（report generator + email automation）在cron中执行

## 问题

业务自动化脚本（如 `auto-tech-trend-generator.py`、`email_automation.py`）需要：
1. 调用外部API（GitHub API via curl）
2. 读写本地文件（reports/, data/）
3. 发送邮件（SMTP或模拟）

在cron模式下，所有执行通道均被阻断：
- `terminal` → tirith安全扫描 pending_approval
- `execute_code` → "BLOCKED: Cron jobs run without a user present to approve"
- `computer_use` → Terminal窗口不存在，无法focus

## 降级策略（按优先级）

### 1. 🔥 主动数据获取（2026-06-22 验证 — 首选）

当脚本无法运行时，不要只做被动诊断。用 `web_search` + `web_extract` 获取实时数据，然后手动生成报告：

**步骤**:
1. `web_search` 搜索目标数据源（如 "GitHub trending repositories today"）
2. `web_extract` 提取聚合页面内容（如 orangebot.ai/github-trending-today）
3. 从提取内容中解析项目列表、排名、语言等
4. `write_file` 生成 JSON 数据文件: `reports/trend_data_YYYYMMDD_090000.json`
5. `write_file` 生成 HTML 报告: `reports/trend_report_YYYYMMDD_090000.html`
6. 更新 `reports/latest_data.json`
7. 追加 `data/run_log.csv` 和 `data/email_log.csv`
8. 写入 `data/daily_status_report_YYYYMMDD.md`

**关键**: 在报告和数据中标注 `data_source: "web_search_fallback"` 和降级说明，避免数据来源混淆。

**优势**: 产出的是**真实报告**而非"BLOCKED"状态消息，对订阅者有实际价值。

**限制**: web_search无法获取精确Star数量，只能获取排名和项目名。在JSON和HTML中标注 `data_quality: "degraded - star counts unavailable"`。

### 2. 文件工具诊断（当主动获取也失败时）
- `read_file` — 检查脚本源码、最新报告、订阅者数据、邮件日志
- `search_files` — 枚举reports/和data/目录，判断系统状态
- `write_file` — 写入状态报告、运行日志、daily-logs

### 3. 状态推断（当脚本无法运行时）
- 检查 `reports/latest_data.json` 的日期字段判断最新报告时间
- 检查 `data/email_log.csv` 的最后几行判断最近发送状态
- 检查 `data/subscribers.csv` 确认订阅者配置完整
- 检查 `data/run_log.csv` 追溯历史执行记录

### 4. 修复建议输出
当检测到cron执行阻断时，在报告中明确给出修复方案：
- **方案A**: Hermes config设置 `approvals.cron_mode: trust`（最简）
- **方案B**: 注册macOS `launchd`定时任务（完全独立于Hermes）
- **方案C**: 用户session手动触发（临时）

## 关键文件路径

| 文件 | 用途 |
|------|------|
| `~/auto-tech-trend-generator.py` | GitHub趋势报告生成器 |
| `~/email_automation.py` | 邮件自动化发送系统 |
| `~/reports/latest_report.html` | 最新HTML报告 |
| `~/reports/latest_data.json` | 最新JSON数据 |
| `~/data/subscribers.csv` | 订阅者列表（5人） |
| `~/data/email_log.csv` | 邮件发送日志 |
| `~/data/run_log.csv` | 系统运行日志 |
| `~/data/daily_status_report_*.md` | 每日状态报告 |

## 数据源参考（主动获取模式）

| 目标数据 | web_search查询 | web_extract目标 |
|---------|---------------|----------------|
| GitHub Trending | "GitHub trending repositories today" | orangebot.ai/github-trending-today |
| AI趋势 | "trending AI GitHub repos 2026" | whatstrending.ai/repos |
| 语言排名 | "TypeScript Python GitHub 2026" | byteiota.com相关文章 |

## 经验教训

1. **先尝试主动获取，再退回被动诊断**：web_search+web_extract可以产出真实报告，比"BLOCKED"有价值得多
2. **不要反复重试被阻断的工具**：terminal连续失败1-2次后应立即切换到web_search方案
3. **run_log.csv是关键**：追加每次执行记录（包括DEGRADED/BLOCKED状态），便于追溯系统健康度
4. **latest_data.json可能滞后**：2026-06-19检查时发现JSON数据停留在06-16，HTML报告在06-18
5. **标注数据质量**：降级模式报告必须标注数据源和质量级别，避免与完整报告混淆
6. **邮件降级标记**：无法实际发送邮件时，在email_log.csv中标记为 `blocked_degraded`，下次用户session补发
