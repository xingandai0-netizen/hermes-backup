# Handling Large Session Files During Daily Log Archival

## 问题
当session消息量超过500条（如1062条消息的antoken优化session），`session_search(session_id=...)` 的READ模式会返回200KB+的JSON文件，存储到临时路径。

## 失败模式
1. `search_files` 在临时JSON文件上搜索关键词 → 只返回1条匹配（整个文件是一行巨型JSON）
2. `read_file` 读取偏移量 → 需要大量调用才能覆盖，且JSON结构不适合逐行阅读
3. 直接解析JSON → cron模式下execute_code被阻断

## 可靠方案：Discovery查询获取定向上下文

对大型session，跳过READ模式，改用DISCOVERY模式+关键词获取关键片段：

```python
# 步骤1：用session主题关键词做discovery查询
session_search(query="antoken 优化 完成 性能", limit=5, sort="newest")

# 步骤2：从bookend_start/bookend_end获取session首尾消息（目标+结论）
# 步骤3：从messages数组获取匹配关键词的上下文片段（±5条消息）
# 步骤4：从snippet获取FTS5高亮摘要
```

## Discovery模式的优势
- 自动提取session的开头（目标）、结尾（结论）、和关键匹配片段
- FTS5高亮snippet直接给出关键上下文
- 输出体积可控（几KB vs 200KB+）
- 不需要execute_code或terminal

## 实战示例（2026-06-27）
antoken session有1062条消息，READ模式返回209KB。改用：
```python
session_search(query="antoken optimization 优化", limit=5, sort="newest")
```
成功获取：session开头（用户问"优化到哪一步了"）、结尾（3个性能瓶颈修复完成+git commit）、关键匹配片段。

## 何时使用此模式
- session消息数 > 200
- session_search READ模式返回的临时文件 > 50KB
- cron模式下无法使用execute_code解析JSON
- 只需要session的摘要而非完整内容（日志归档场景）
