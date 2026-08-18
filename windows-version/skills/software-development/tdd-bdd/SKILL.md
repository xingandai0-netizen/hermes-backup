---
name: tdd-bdd
description: "Test-driven development (TDD) and behavior-driven development (BDD) enforcement. RED-GREEN-REFACTOR cycle, BDD scenario writing, AI coding constraints. Use when user wants TDD, BDD, test-first development, red-green-refactor, or when enforcing test discipline on AI-generated code."
version: 1.0
tags: [tdd, bdd, testing, red-green-refactor, ai-coding, discipline]
---

# TDD/BDD Enforcement

## 核心原则

### TDD: RED → GREEN → REFACTOR
1. **RED**: 先写一个会失败的测试
2. **GREEN**: 写最少的代码让测试通过
3. **REFACTOR**: 重构代码，保持测试通过

### BDD: 场景驱动
```gherkin
Feature: 用户登录
  Scenario: 邮箱密码登录
    Given 用户在登录页面
    When 输入有效邮箱和密码
    And 点击登录按钮
    Then 跳转到工作空间
    And 显示用户信息
```

## 强制规则

### 所有代码任务必须遵守
1. **先写测试再写实现** — 不能跳过RED阶段
2. **每个功能点一个测试** — 不要写巨型测试
3. **测试必须先失败** — 确认测试能检测到问题
4. **实现后测试必须通过** — 不能留红灯
5. **重构后重新运行全部测试** — 确保没有破坏

### AI编码特别约束
- AI容易"声称完成但实际没改" — 必须验证
- `patch` 可能静默失败 — 用 `search_files` 确认
- 每次修改后必须 `npm run build` + `npm test`
- 不能用"构建通过"代替"功能测试"

## 测试金字塔

```
       /  E2E  \        少量，验证关键路径
      / 集成测试 \       适量，验证模块协作
     /  单元测试  \      大量，验证独立功能
```

### 单元测试（Vitest/pytest）
```typescript
// 前端
describe('usePollPublicUrl', () => {
  it('should abort on unmount', () => {
    const { unmount } = renderHook(() => usePollPublicUrl(url))
    unmount()
    expect(abortSpy).toHaveBeenCalled()
  })
})
```

```python
# 后端
def test_credit_deduct():
    result = deduct_credits(user_id, 10)
    assert result.remaining == 90
```

### BDD 场景（.feature 文件）
```gherkin
Feature: 文件上传
  Scenario: 上传图片获取公开URL
    Given 用户已登录
    When 上传一张PNG图片
    Then 返回asset_id
    And 轮询公开URL最终可访问
```

## 常见陷阱

### 1. 测试不验证行为只验证结构
```typescript
// ❌ 只验证函数存在
expect(typeof handler).toBe('function')

// ✅ 验证行为
expect(handler(input)).toBe(expectedOutput)
```

### 2. Mock过多导致测试无意义
只mock外部依赖（API、数据库），不要mock被测函数的内部逻辑。

### 3. 测试命名不清晰
```typescript
// ❌ 
it('works', () => {})

// ✅
it('should abort polling when component unmounts', () => {})
```

## Consolidated From
| Former Skill | Content |
|---|---|
| `tdd` | RED-GREEN-REFACTOR cycle, test-first development |
| `test-driven-development` | TDD enforcement, Vitest patterns |
| `tdd-bdd-enforcement` | BDD scenarios, AI coding constraints, discipline rules |
| `tdd-bdd-ai-coding-report` | TDD/BDD约束AI写代码调研报告 |
