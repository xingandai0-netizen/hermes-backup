# Session Search Query Patterns

在cron自动归档时，按以下顺序执行搜索以确保覆盖面：

## 基础查询（必做）
```
session_search(query="YYYY-MM-DD", limit=10)
```

## 补充查询（根据当日活动调整）
从基础查询的summary中提取主要项目名，再搜索：
```
session_search(query="YYYY-MM-DD studio OR antokex OR 项目名", limit=5)
```

## 跨午夜检测
注意结果中 `when` 字段为前一天 22:00+ 的session，如果summary内容属于今天的任务流，应归入今天日志。

示例：`session_id="20260515_225446_639e13"` 开始于5/15晚22:54，但任务是Studio v8优化（延续到5/16），应归入5/16日志。

## 结果去重
session_search可能在不同查询中返回同一session（不同关键词匹配）。用session_id去重。

## Summary质量
- Cron session的summary通常较长且结构化，直接提取关键信息即可
- CLI session的summary可能较短，需要从上下文推断

## 大型Session处理
当日session消息数 > 200时，READ模式会生成巨型JSON文件（200KB+），无法有效搜索。改用DISCOVERY模式+关键词获取定向上下文。详见 `references/large-session-handling.md`。
