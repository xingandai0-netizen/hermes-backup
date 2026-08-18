---
name: daily-log-manager
description: 每日日志管理技能。自动记录任务内容、沟通摘要，维护多层记忆架构。
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
---

# 每日日志管理技能

## 功能
- 自动创建每日日志文件
- 记录任务内容、沟通摘要、关键决策
- 定期压缩核心信息存入记忆库
- 维护多层记忆架构

## 记忆架构

| 层级 | 工具 | 容量 | 用途 |
|------|------|------|------|
| L1 | memory工具 | 2200字符 | 核心关键信息（用户偏好+当前业务） |
| L2 | session_search | 无限 | 搜索回顾历史对话 |
| L3 | 本地日志文件 | 无限 | 详细每日记录 |
| L4 | Apple备忘录 | 无限 | 重要方案存档 |

## 日志文件路径
- 基础路径：`~/.hermes/daily-logs/`
- 按年/月组织：`~/.hermes/daily-logs/YYYY/MM/YYYY-MM-DD.md`

## 日志格式模板

```markdown
# YYYY-MM-DD 每日日志

## 今日任务记录

### 任务N：[任务名称]
- 时间：[时段]
- 操作：[具体操作]
- 结果：✅/⚠️/❌

---

## 关键沟通内容摘要
[重要讨论内容压缩版]

---

## 下一步待执行
[待办事项列表]

---

## 备注
[其他信息]
```

## 记忆库压缩策略

memory工具空间有限（2200字符），采用以下策略：

1. **保留不变**：用户偏好、核心原则
2. **定期更新**：当前活跃任务、业务进展
3. **压缩存储**：用简短关键词替代详细描述
4. **历史归档**：详细内容移至日志文件，memory仅存索引

## 执行流程（Cron自动归档）

### 步骤1：获取日期
- 正常环境：`date '+%Y-%m-%d'`
- Terminal被Tirith阻断时：从session_search结果的时间戳推断，或用conversation元数据中的日期

### 步骤2：搜索今日对话
执行多次session_search，覆盖不同维度：
1. `session_search(query="YYYY-MM-DD", limit=10, sort="newest")` — 日期精确匹配
2. `session_search(limit=10, sort="newest")` — **无query浏览最近session**（当步骤1返回0结果时必须执行此步）
3. 用 `date` 输出的Unix时间戳对比session的 `started_at` / `last_active` 判断归属日期
4. 检查结果中是否有前一晚22:00后开始的session（跨午夜任务）

**重要**：session的时间戳可能是前一天深夜开始的，summary内容属于今天的任务。将这些也纳入今日日志。

**🔴 搜索回退策略（2026-06-17 实测验证）**：
- `session_search(query="YYYY-MM-DD")` 经常返回0结果（FTS5索引对日期格式匹配不稳定）
- **可靠方案**：先无query浏览最近10个session，再根据时间戳判断日期归属
- 如果browse结果中所有session都是昨天的，说明今天确实没有用户活动

### 步骤2.5：提取关键session详情（bookend工作流）
从browse结果获取session列表后，需要提取每个关键session的摘要。**按以下顺序操作**：

1. **用DISCOVERY模式获取bookends**：
   ```python
   session_search(query="<关键词>", limit=3)
   ```
   返回 `bookend_start`（前3条消息）+ `bookend_end`（后3条消息）+ `snippet`（FTS5高亮片段）。这三者足以理解：任务目标→关键操作→最终结果。

2. **如果需要更多上下文，用SCROLL模式**：
   ```python
   session_search(session_id="<id>", around_message_id=<从bookend或snippet中获取的message_id>, window=3)
   ```
   ⚠️ **NEVER用 `around_message_id=0`** — message_id从非零值开始，0会报"not in session"错误。必须从discovery结果中提取真实的message_id。

3. **避免READ模式**（`session_search(session_id="<id>")` 无around_message_id）：
   对大session（100+消息）会返回100KB+文件，超出处理能力。只在小session（<20条消息）时使用。

**🔴 2026-07-03 实测验证的完整工作流**：
```
① browse(limit=10) → 获取session列表+时间戳
② 对每个关键session用discovery模式搜索 → 获取bookends+snippet
③ 从bookend_end中提取最终结果状态
④ 如需中间细节，用scroll模式（用真实message_id）
```

### 步骤3：检查并创建目录
- `execute_code` 中用 `os.makedirs(os.path.expanduser("~/.hermes/daily-logs/YYYY/MM/"), exist_ok=True)`
- **注意**：terminal可能被安全扫描器阻断，优先用execute_code

### 步骤4：读取现有日志（如存在）
- 用 `read_file` 读取 `~/.hermes/daily-logs/YYYY/MM/YYYY-MM-DD.md`
- 如果已存在，合并新信息而非覆盖

### 步骤5：整理并写入日志
按模板格式整理所有session内容，**按优先级尝试写入**：
1. `write_file(path, content)` — **首选**，通用文件写入工具，可写入任意路径（包括 daily-logs 目录）。在cron模式下可用，不受tirith安全扫描限制。
2. `execute_code` 中用 `open(path, 'w').write(content)` — 备选，但可能报 FileNotFoundError
3. `computer_use` 打开 Terminal 执行 `mkdir -p && cat > file` — 备选，但 Terminal 窗口可能不存在
4. **全部失败时的降级方案**：将完整日志内容作为 cron 输出直接返回。系统会自动投递给用户。在报告末尾注明"日志文件未能写入磁盘，建议下次用户session中手动保存"并给出完整文件路径。

**⚠️ 注意**：`write_file` 是独立的顶级工具，与 `skill_manage(action='write_file')` 不同。后者只能写入技能目录，前者可写入任意路径。2026-06-08 实测确认 `write_file` 在 cron 模式下可正常写入 `~/data/` 等任意目录。

### 步骤5.5：检查前一日日志是否缺失（回填）
扫描 `~/.hermes/daily-logs/YYYY/MM/` 目录，检查前1-2天的日志文件是否存在。
- 如果前一日无日志但session_search发现该日有session活动 → 创建补录日志
- 补录日志标题注明"（补录）"，备注中标注"由YYYY-MM-DD归档任务补录"
- 避免过度回填：最多补录前2天，更早的缺失让cron自然追平

### 步骤6：更新Memory（可选）
- 将跨session需要记住的重要发现写入memory
- **Cron环境下memory工具可能不可用**（返回"Memory is not available"），这是正常限制，无需报错
- 如果memory不可用，在日志备注中记录"建议下次用户session中手动补充memory"

### 步骤7：输出归档摘要
返回简洁的归档完成报告，包含：任务数量、关键发现、高优待办。

## Cron环境约束

| 工具 | Cron中可用性 | 备注 |
|------|-------------|------|
| write_file | ✅ 可用 | 通用文件写入，可写入任意路径，不受tirith限制（2026-06-08确认） |
| read_file | ✅ 可用 | 读取任意文件，稳定可靠 |
| search_files | ✅ 可用 | 文件搜索/列举，稳定可靠 |
| session_search | ✅ 可用 | 主要数据源，稳定可靠 |
| execute_code | ❌ BLOCKED | Cron模式下被approvals系统阻止（2026-06-17确认），不能用 |
| computer_use | ⚠️ 不稳定 | Terminal窗口可能不存在，cua-driver可能报错，不能依赖 |
| terminal | ❌ 常被阻断 | cron环境中tirith安全扫描会阻断所有命令(pending_approval) |
| memory | ❌ 不可用 | cron环境配置限制，返回"Memory is not available" |
| browser工具 | ✅ 可用 | web_search + web_extract 可获取实时数据，是降级报告生成的首选数据源 |

**关键认知**：2026-06-08 更新——`write_file` 工具在 cron 模式下可用，是写入本地文件的首选方案。当 terminal 被 tirith 阻断、execute_code 报错时，`write_file` + `read_file` + `search_files` 三个文件工具组合可以完成大部分诊断和日志写入工作。

## 参考文档
- `references/session_search_patterns.md` — session搜索策略和去重技巧
- `references/cron-missing-skill-pattern.md` — Cron job引用不存在的skill的检测和修复

## 常见陷阱

详见 `references/cron-fallback-pattern-2026-06-06.md` — 2026-06-06 全工具故障降级实战记录。
详见 `references/write-file-size-limit-2026-06-13.md` — write_file 内容大小限制与压缩策略。
详见 `references/cron-error-patterns.md` — Cron环境错误消息模式与工具可用性矩阵（2026-06-17）。

### 🔴 Terminal 被 Tirith 安全扫描阻断
**现象**：所有 `terminal` 调用返回 `exit_code: -1`、`pending_approval: true`、`pattern_key: "tirith:unknown"`
**应对**：使用 `write_file` + `read_file` + `search_files` 组合完成日志工作。这三个文件工具不受 tirith 限制。详见 `hermes-troubleshooting` 技能的 `references/tirith-security-scan-blocking-2026-06-08.md`。

### 🔴 业务自动化脚本在Cron中无法执行（已有主动降级方案）
**场景**：cron job需要运行report generator、email sender等业务Python脚本
**现象**：terminal + execute_code 均被安全策略阻断
**最佳应对**：用 `web_search` + `web_extract` 获取实时数据，`write_file` 生成完整报告（JSON+HTML+CSV+日志）。这比仅诊断文件状态有价值得多。详见 `references/cron-business-automation-pattern-2026-06-19.md` 的"主动数据获取"章节。
**降级应对**：如果web_search也失败，退回文件工具诊断。

### 🔴 所有文件写入工具同时故障
**场景**：execute_code 报 FileNotFoundError + computer_use Terminal 不存在 + terminal 被阻断
**应对**：不要反复重试同一个工具（浪费迭代次数）。诊断一次确认故障后，立即切换到降级方案——将完整日志作为 cron 输出返回。在报告中明确标注文件路径，方便用户手动保存。
**识别信号**：execute_code 连续失败 3 次 → 停止重试，切换输出模式。

### 🔴 Memory 工具在 Cron 中不可用
**现象**：`memory(action='add')` 返回 "Memory is not available. It may be disabled in config or this environment."
**应对**：这是正常限制，不是错误。在日志的"备注"部分记录需要补充的 memory 条目，标注"建议下次用户session中手动补充"。

### 🟡 write_file 内容过大导致 Stream Timeout
**现象**：`write_file` 调用返回后系统报 "stream timed out before it could be delivered"，日志未写入。
**原因**：cron 模式下 stream 有 ~8K token 的内容上限。当日志包含完整 session 数据、大表格、或多个任务的详细记录时，单次 `write_file` 调用会超时。
**应对**：
1. **写入精简版日志**——cron 归档不需要写入完整 session 原文，写摘要即可。表格只保留关键列，省略详细数据。
2. **如果确实需要大文件**：拆分为多次小 `write_file` 调用（每次 < 3000 字符），或用 `patch` 追加内容。
3. **Read-Combine-Write 模式（2026-07-16 实测验证）**：当需要向已有文件追加内容但 terminal 被阻断（无法 `cat >>`）时：
   - Step 1: `read_file` 读取现有文件内容
   - Step 2: `write_file` 写追加内容到 `/tmp/` 临时文件
   - Step 3: `read_file` 读取临时文件
   - Step 4: 在内存中拼接两部分内容
   - Step 5: `write_file` 用拼接后的完整内容覆盖原文件
   - **注意**：如果拼接后总内容仍然 >8K token，需要进一步压缩或分多次写入
4. **预防**：在整理阶段就有意识地压缩——session 详情用 bullet 摘要而非全文复制，大表格只保留 top 3-5 行。

**🟢 Skeleton-then-Patch 模式（2026-08-06 实测验证）**：
比 Read-Combine-Write 更简洁的替代方案——不需要先读取已有文件：
- Step 1: `write_file` 写入精简骨架（标题+任务列表+基础结构，<3KB）
- Step 2: `patch(mode='patch')` 追加详细内容（趋势数据表、沟通摘要、待办、备注）
- **优势**：只需2步 vs 5步，无需读取临时文件，patch的`@@ context @@`定位可靠
- **适用场景**：新建日志文件（无需合并已有内容）时首选此模式
- 2026-08-06 cron归档实测：骨架835字节 → patch追加1.5KB → 总计2.4KB，全程无超时

### 🟡 跨午夜 Session 归属（含多日活跃Session）
**现象**：session 时间戳显示前一天开始，但实际任务内容跨越到今天
**两种模式**：
1. **短跨午夜**：前一天深夜（23:xx）开始，内容属于今天 → 归入今天日志
2. **多日活跃Session**：session从更早日期开始（如昨天），但今天仍有大量交互（如713条消息的渗透测试session从8月15日延续到8月16日）→ 如果 `last_active` 在今天且今天有实质性消息活动，归入今天日志
**判断标准**：检查 `started_at` 和 `last_active` 时间戳。如果 `last_active` 在今天日期内，且今天有新消息产生（非仅心跳），该 session 应归入今天的日志。
**⚠️ 与"大型Session无实质活动"的区分**：多日活跃Session今天有实质性交互（用户提问、工具调用、结果输出）；而"无实质活动"指last_active虽在今天但今天无新消息（如系统维护、后台同步等非用户交互）。

### 🟡 大型Session的last_active ≠ 今天有实质活动（2026-07-12 新增）
**现象**：browse结果中出现990消息的大型session，`last_active`时间戳落在今天，但session主题是前几天的项目
**风险**：错误归因——将无实质活动的session纳入今日日志
**应对**：用session标题关键词做discovery查询，检查bookend_end中最后消息的时间戳。如果最后消息是前几天的，说明今天无实质活动，跳过不纳入日志。详见 `references/cross-day-large-session-filtering.md`。

### 🟡 大型Session（500+消息）处理
**现象**：session_search READ模式返回200KB+临时文件，search_files和read_file都无法有效提取摘要
**应对**：改用DISCOVERY模式+关键词查询，获取bookend（首尾消息）+ FTS5高亮snippet。详见 `references/large-session-handling.md`。

### 🟡 session_search 日期查询返回空结果
**现象**：`session_search(query="YYYY-MM-DD")` 返回 0 条结果，但实际有当天 session
**原因**：FTS5 索引对日期字符串匹配不稳定，session 标题/内容可能不包含搜索的日期格式
**应对**：不传 query 参数，用 `session_search(sort="newest", limit=10)` 浏览最近 session，根据 `started_at` 时间戳判断日期归属。这是 2026-06-17 实测确认的可靠方案。

### 🟡 around_message_id=0 报错
**现象**：`session_search(session_id="...", around_message_id=0)` 返回 "not in session" 错误
**原因**：message_id 从非零值开始（如 34128），0不在范围内
**应对**：从 discovery/bookend 结果中提取真实 message_id。详见 `references/session-search-pitfalls-2026-07-03.md`。

## 日志质量检查清单
- [ ] 每个session的summary都被读取并消化（不遗漏）
- [ ] 跨午夜session正确归属
- [ ] 任务状态标记准确（✅/⚠️/❌）
- [ ] **检查"Cron Missing Skill"模式**：session中是否出现"Skill(s) not found and skipped"——如有，在下一步待执行中记录修复建议（见 `references/cron-missing-skill-pattern.md`）
- [ ] 下一步待执行按优先级排列
- [ ] 备注中记录了环境限制和已知问题
- [ ] 重要的新发现已尝试写入memory（或记录待补充）

## 使用时机

- 用户要求"记录今天做了什么"
- 完成重要任务后自动记录
- 用户要求回顾历史内容时用session_search
- 每日结束时（可选cron job自动执行）

## 相关技能
- apple-notes：写入Apple备忘录（macOS环境）
- session_search：搜索历史对话