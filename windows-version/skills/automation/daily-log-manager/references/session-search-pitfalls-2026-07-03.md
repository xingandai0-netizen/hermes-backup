# Session Search Pitfalls — 2026-07-03 实测记录

## ❌ around_message_id=0 总是失败

**现象**：`session_search(session_id="...", around_message_id=0)` 返回 `"error": "around_message_id 0 not in session_id ..."`

**原因**：message_id 从非零值开始（如 34128），0不在任何session的ID范围内。

**正确做法**：从 discovery 结果的 `bookend_start` / `bookend_end` / `messages` 数组中提取真实的 `id` 字段作为 `around_message_id`。

---

## ❌ READ模式对大session返回超大文件

**现象**：`session_search(session_id="<大session>")` 返回 120KB+ 的 persisted-output，需要额外 read_file 调用才能处理。

**2026-07-03 实测**：
- Antoken session (2128消息) → READ模式不可用
- Rental Deposit session (86消息) → 返回123,669字符

**正确做法**：
- 小session (<20消息)：可用READ模式
- 大session：用DISCOVERY模式搜索关键词，获取 bookend_start + bookend_end + snippet

---

## ✅ 可靠的bookend提取工作流

```
# 1. 先用关键词搜索获取bookends
session_search(query="Antoken Pointer Events Bug", limit=3)
→ 返回 bookend_start (前3条) + bookend_end (后3条) + snippet

# 2. bookend_end 包含最终结果状态
# 3. snippet 包含 FTS5 高亮的匹配片段
# 4. 三者组合足以理解：目标→操作→结果

# 5. 如需更多上下文，用真实message_id scroll
session_search(session_id="...", around_message_id=38589, window=3)
```

---

## ✅ 无query browse 是最可靠的session发现方式

`session_search(limit=10, sort="newest")` 返回最近10个session的：
- session_id, title, source, started_at, last_active
- message_count, preview

然后根据 started_at 时间戳判断日期归属。这比日期关键词搜索可靠得多。

---

## Cron模式下工具可用性确认 (2026-07-03)

| 工具 | 状态 |
|------|------|
| session_search | ✅ 所有模式均可用 |
| write_file | ✅ 可写入任意路径 |
| read_file | ✅ 可读取任意文件 |
| search_files | ✅ 可搜索文件 |
| memory | ❌ "Memory is not available" |
| terminal | ❌ Tirith pending_approval |
| execute_code | ❌ 被阻断 |
