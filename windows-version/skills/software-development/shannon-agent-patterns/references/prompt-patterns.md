# Shannon Agent Prompt 设计模式

从 Shannon 的 prompt 模板中提取的 Agent 指令设计模式。

## Prompt组装方式

Shannon用模板引擎组装prompt：
```
{{SHARED_TARGET}}      → 目标信息
{{SHARED_RULES}}       → 通用规则
{{SHARED_VULN_SCOPE}}  → 漏洞范围定义
{{SHARED_EXPLOIT_SCOPE}} → 利用范围定义
{{AGENT_SPECIFIC}}     → Agent专属指令
```

这种模式让prompt可维护、可复用。

## 关键设计原则

### 1. 角色明确
每个Agent有明确的角色定义，不模糊。

### 2. 约束清晰
- 能做什么（scope）
- 不能做什么（rules of engagement）
- 产出什么（deliverable）

### 3. 证据要求
- 结论必须有工具输出支撑
- 不允许编造或推测
- 每个发现必须有PoC

### 4. 判定标准
```
EXPLOITED: 成功证明影响
BLOCKED_BY_SECURITY: 有效漏洞但被WAF阻止
OUT_OF_SCOPE_INTERNAL: 需要内部访问（不追）
FALSE_POSITIVE: 实际不脆弱
```

### 5. 边界约束
- 只从外部网络测试
- 不尝试内部网络访问
- 不尝试直接服务器访问
- 不尝试数据库控制台访问

## 应用到Hermes的delegate_task

### 模板：安全研究任务
```
goal: "对{目标}进行{漏洞类型}分析"
context: |
  目标URL: {url}
  范围: {scope}
  规则: 只从外部测试，不尝试内部访问
  产出物: {output_path}
  
  判定标准:
  - EXPLOITED: 成功证明
  - BLOCKED: 被防护阻止
  - FALSE_POSITIVE: 实际不脆弱
  
  证据要求: 每个结论必须附带工具输出
toolsets: ['terminal', 'web', 'browser']
```

### 模板：代码开发任务
```
goal: "实现{模块}的{功能}"
context: |
  架构: {architecture}
  接口: {interface_spec}
  产出物: {output_path}
  
  质量要求:
  - 代码可运行
  - 有测试覆盖
  - 有错误处理
  
  验证方式: 运行测试并附带输出
toolsets: ['terminal', 'file', 'coding']
```

### 模板：调研分析任务
```
goal: "调研{主题}的{方面}"
context: |
  调研范围: {scope}
  关注点: {focus_areas}
  产出物: {output_path}
  
  质量要求:
  - 数据有来源
  - 结论有依据
  - 对比有表格
  
  验证方式: 附带原始数据来源
toolsets: ['web', 'browser', 'file']
```
