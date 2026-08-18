# Cron 全工具故障降级模式 — 2026-06-06 实战记录

## 故障现象

当天所有 4 个 cron session 中，文件写入相关的工具全部不可用：

| 工具 | 错误信息 | 根因 |
|------|---------|------|
| execute_code | `FileNotFoundError: [Errno 2]` | Python venv 路径损坏或丢失 |
| computer_use capture | `capture failed: ` (空错误) | 无可用窗口 |
| computer_use focus_app | `no on-screen window matched app='Terminal'` | Terminal 未打开 |
| computer_use type (cmd+space) | `cua-driver error:` | cua-driver 连接异常 |
| memory | `Memory is not available` | cron 配置限制 |

## 降级执行流程

```
1. session_search(query="YYYY-MM-DD", limit=10) → ✅ 获取 4 个 session 数据
2. session_search(limit=5) → ✅ 浏览最近 session 列表
3. 尝试 execute_code 读取现有日志 → ❌ FileNotFoundError
4. 尝试 computer_use 打开 Terminal → ❌ 无窗口
5. 尝试 memory 记录关键信息 → ❌ 不可用
6. ✅ 降级：将完整日志作为 cron 输出文本返回
```

## 关键经验

1. **不要反复重试失败工具** — execute_code 连续失败 3 次后应立即切换策略
2. **session_search 是最可靠的 cron 工具** — 在所有其他工具故障时仍可用
3. **降级输出是可接受的** — 系统会自动将 cron 输出投递给用户，内容不丢失
4. **在降级报告中给出完整文件路径** — 方便用户在下次 session 中手动保存
