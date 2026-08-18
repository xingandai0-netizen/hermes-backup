# Shannon 重试与错误处理模式

## 错误分类

### 可重试错误（Transient）
- 网络超时
- API限流（rate limit）
- 临时服务不可用
- Docker容器启动失败

### 不可重试错误（Permanent）
- AuthenticationError（认证失败）
- ConfigurationError（配置错误）
- InvalidTargetError（目标无效）
- PermanentError（永久错误）

### 需要判断的错误
- GitError（可能是临时的）
- AgentExecutionError（取决于具体错误）

## 重试策略

### 生产环境
```javascript
{
  initialInterval: '5分钟',      // 首次等待
  maximumInterval: '30分钟',     // 最大等待
  backoffCoefficient: 2,         // 指数退避
  maximumAttempts: 50,           // 最大重试次数
}
```

### 测试环境
```javascript
{
  initialInterval: '10秒',
  maximumInterval: '30秒',
  backoffCoefficient: 2,
  maximumAttempts: 5,
}
```

### 预检验证
```javascript
{
  initialInterval: '10秒',
  maximumInterval: '1分钟',
  backoffCoefficient: 2,
  maximumAttempts: 3,
}
```

## 应用到Hermes

### delegate_task的重试策略
```python
# 网络任务：高重试
delegate_task(
    goal="...",
    # 如果失败，手动重试最多3次，间隔递增
)

# 认证任务：不重试
delegate_task(
    goal="...",
    # 如果认证失败，直接报错
)

# 开发任务：修改后重试
delegate_task(
    goal="...",
    # 如果失败，分析错误后修改参数重试
)
```

### 失败处理
```
1. 区分错误类型
2. 可重试 → 等待后重试
3. 不可重试 → 报告错误，跳过该分支
4. 需要判断 → 分析错误原因后决定
5. 所有分支失败 → 报告整体失败
```

## 管线容错

Shannon的关键设计：**单个管线失败不影响其他管线**

```
Pipeline 1: injection-vuln → injection-exploit  ✅ 成功
Pipeline 2: xss-vuln → xss-exploit              ❌ 失败（继续）
Pipeline 3: auth-vuln → auth-exploit             ✅ 成功
Pipeline 4: ssrf-vuln → ssrf-exploit             ❌ 失败（继续）
Pipeline 5: authz-vuln → authz-exploit           ✅ 成功

Report: 基于3个成功的管线生成报告，标注2个失败的管线
```

**应用到Hermes：**
并行delegate_task时，允许部分失败。
汇总时标注哪些成功、哪些失败、失败原因。
不要因为一个分支失败就放弃整个任务。
