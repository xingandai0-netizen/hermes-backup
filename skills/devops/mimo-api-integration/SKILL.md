---
name: mimo-api-integration
description: |
  小米MiMo模型API集成指南。覆盖OpenAI/Anthropic双协议接入、
  推理模型(reasoning model)流式输出格式、SSE解析陷阱等。
  基于api.tokex.top中转站和ClaudeChat桌面应用的实战经验。
tags: [mimo, xiaomi, api, streaming, sse, reasoning, openai, anthropic, tokex]
version: 1.2
created: 2026-05-08
updated: 2026-08-16
---

# MiMo API 集成指南

## 0. 采购状态 [2026-05-13更新]

✅ **MiMo官方API平台已公开**: https://platform.xiaomimimo.com
- 定价文档: https://platform.xiaomimimo.com/static/docs/pricing.md
- Token Plan预付费套餐制，需小米账号注册
- TTS系列限时免费
- 详细定价见本skill `references/mimo-official-pricing.md`

---

### 确认可用模型（通过 GET /v1/models 获取）
| 模型ID | 类型 | 特点 |
|--------|------|------|
| mimo-v2.5-pro | 推理模型 | 输出 reasoning_content + content 双阶段 |
| mimo-v2.5 | 标准模型 | 普通对话 |
| mimo-v2-pro | 推理模型 | 推理+内容双阶段 |
| mimo-v2-omni | 多模态 | 支持图片等 |

### TTS 模型 (全部限时免费, 按token计费)
mimo-v2-tts, mimo-v2.5-tts, mimo-v2.5-tts-voiceclone, mimo-v2.5-tts-voicedesign
- 上下文: 8K, 最大输出: 8K, RPM: 100, TPM: 10M
- TTS通过 `/v1/chat/completions` 调用(非 `/v1/audio/speech`)，需在messages中包含assistant role

### 不可用模型（GET /v1/models 会列出但 chat completions 400）
- mimo-v2-flash：报 "Not supported model mimo-v2-flash"

### ⚠️ 之前错误记录的模型名（不存在）
- ❌ mimo-v2.5-tts-flash — 不存在
- ❌ mimo-v2-omni-tts — 不存在  
- ❌ mimo-v2-omni-tts-flash — 不存在
- ❌ mimo-v2-tts-flash — 不存在
- ❌ mimo-v2-flash — GET /v1/models 列出但 chat 不支持

## 2. API 端点

### 通过 api.tokex.top 中转站

```
OpenAI 协议:    POST https://api.tokex.top/v1/chat/completions
Anthropic 协议: POST https://api.tokex.top/v1/messages
模型列表:       GET  https://api.tokex.top/v1/models
```

### ⚠️ 关键陷阱：Anthropic 端点

```
❌ /anthropic/v1/messages → 返回 HTML（网页界面），不是 API
✅ /v1/messages           → 返回正确的 Anthropic 协议响应
```

Claude CLI 无法通过此中转站工作，原因：
1. Claude CLI 硬编码 Claude 模型名校验，拒绝非 Claude 模型名
2. Claude CLI 使用 /anthropic/v1/messages 路径（返回 HTML）

### 上游直连（小米官方）
```
base_url: https://token-plan-cn.xiaomimimo.com/v1 (OpenAI)
base_url: https://token-plan-cn.xiaomimimo.com/anthropic (Anthropic)
```

## 3. ⚠️ 推理模型流式输出格式（关键）

MiMo 推理模型（mimo-v2.5-pro, mimo-v2-pro）的流式输出分两个阶段：

### 阶段1：推理过程
```json
{"choices":[{"delta":{"reasoning_content":"The user wants me to..."}}]}
{"choices":[{"delta":{"reasoning_content":" respond warmly"}}]}
```

### 阶段2：最终回答
```json
{"choices":[{"delta":{"content":"Hello"}}]}
{"choices":[{"delta":{"content":"!"}}]}
```

### 首个 chunk 特殊情况
第一个 chunk 的 `content` 是空字符串 `""`：
```json
{"choices":[{"delta":{"content":"","role":"assistant"}}]}
```

### SSE 解析器必须同时处理两种字段

```swift
// Swift 示例 — OpenAI SSE parser
public static func parse(line: String) -> String? {
    // ... 解析 SSE line 到 delta dict ...
    
    // 优先取 content（最终回答），降级到 reasoning_content（推理过程）
    if let content = delta["content"] as? String, !content.isEmpty {
        return content
    }
    if let reasoning = delta["reasoning_content"] as? String, !reasoning.isEmpty {
        return reasoning
    }
    return nil
}
```

```python
# Python 示例
def parse_sse_line(line: str) -> str | None:
    if not line.startswith("data: "):
        return None
    data = json.loads(line[6:])
    delta = data["choices"][0]["delta"]
    # 优先 content，降级 reasoning_content
    content = delta.get("content", "")
    if content:
        return content
    reasoning = delta.get("reasoning_content", "")
    if reasoning:
        return reasoning
    return None
```

### 用户体验影响

如果只解析 `content`：
- 推理阶段用户看到空白（等待）
- 最终回答阶段才开始显示文字
- 体验差：长推理模型可能等 10-30 秒无反馈

如果同时解析 `reasoning_content`：
- 推理阶段实时显示推理过程
- 最终回答阶段无缝切换
- 体验好：用户始终看到进展

## 4. 标准模型 vs 推理模型

| | 标准模型 (mimo-v2.5) | 推理模型 (mimo-v2.5-pro) |
|---|---|---|
| 流式输出 | 只有 content | reasoning_content + content |
| 响应速度 | 快 (~2-5s) | 慢 (~15-35s) |
| Token 消耗 | 正常 | 高（推理 tokens 也算） |
| 适用场景 | 日常对话 | 复杂推理、编码 |

## 4.5 TTS API 调用方式

MiMo TTS模型通过 `/v1/chat/completions` 调用，**不是** `/v1/audio/speech`：
- `/v1/audio/speech` → 404 Not Found
- `/v1/chat/completions` → 正确，但需要特殊格式

请求要求: messages中必须包含assistant role（"messages must contain an assistant role for TTS model"）

具体调用格式参见官方文档:
- V2.5-TTS: https://platform.xiaomimimo.com/static/docs/usage-guide/speech-synthesis-v2.5.md
- V2-TTS: https://platform.xiaomimimo.com/static/docs/usage-guide/speech-synthesis.md

## 5. Anthropic 协议接入

MiMo 支持 Anthropic 协议（通过中转站 `/v1/messages`），
但 Claude CLI 无法使用（模型名校验问题）。

自定义客户端可以使用 Anthropic 协议：
```bash
curl -X POST https://api.tokex.top/v1/messages \
  -H "x-api-key: YOUR_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"mimo-v2.5-pro","max_tokens":100,"messages":[{"role":"user","content":"hi"}]}'
```

## 6. 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| "empty or malformed response" | 用了 /anthropic/v1/messages | 改用 /v1/messages |
| "Not supported model mimo-v2-flash" | 该模型不支持 chat | 从可用列表移除 |
| 流式输出无内容 | parser 只取 content | 加 reasoning_content 支持 |
| 首个 chunk 空字符串 | content=\"\" 初始化 | filter 掉空字符串 |
| Claude CLI 拒绝模型名 | CLI 硬编码 Claude 模型 | 不用 CLI，直接 HTTP |
| reasoning_content 显示在聊天 UI | Agent/Chat 模式未区分 | Agent 模式只显示 content，隐藏推理过程 |

## 7. OpenAI Function Calling（工具调用）

MiMo 完整支持 OpenAI function calling 协议，可用于构建 Agent 系统。

### 验证状态
✅ 2026-05-08 实测通过，mimo-v2.5-pro 通过 api.tokex.top 返回标准 tool_calls

### 请求格式
```json
{
  "model": "mimo-v2.5-pro",
  "messages": [{"role":"user","content":"list files in /tmp"}],
  "tools": [{
    "type": "function",
    "function": {
      "name": "terminal",
      "description": "Execute a shell command",
      "parameters": {
        "type": "object",
        "properties": {
          "command": {"type": "string", "description": "Shell command to run"}
        },
        "required": ["command"]
      }
    }
  }],
  "stream": true
}
```

### 响应格式（流式 tool_calls）

工具调用分多个 chunk 传输：
```
data: {"choices":[{"delta":{"tool_calls":[{"index":0,"id":"call_xxx","type":"function","function":{"name":"terminal","arguments":""}}]}}]}
data: {"choices":[{"delta":{"tool_calls":[{"index":0,"function":{"arguments":"{\"co"}}]}}]}
data: {"choices":[{"delta":{"tool_calls":[{"index":0,"function":{"arguments":"mmand\":\"ls\"}"}}]}}]}
data: {"choices":[{"finish_reason":"tool_calls"}]}
```

关键：
- `id` 和 `name` 只在第一个 chunk 出现
- `arguments` 是逐步拼接的（JSON 片段）
- 需要自己缓冲拼接完整 JSON
- `finish_reason` 为 `"tool_calls"` 而非 `"stop"`

### 工具结果提交
```json
{
  "role": "tool",
  "tool_call_id": "call_xxx",
  "content": "file1.txt\nfile2.txt\n"
}
```

### Agent Loop 模式
```
用户输入 → mimo(tool_calls) → 执行工具 → 结果送回 mimo → 循环
```
- `finish_reason == "stop"` 时循环结束，content 是最终回答
- `finish_reason == "tool_calls"` 时继续循环
- 建议限制最大 10 轮防止死循环

### UI 设计注意事项
- Agent 模式：reasoning_content 应隐藏（不显示在聊天气泡），只显示最终 content
- Chat 模式：可以显示 reasoning_content 作为思考过程
- 工具执行状态需要在 UI 上展示（如 "Running: ls -la"）

## 8. MiMo 定价与获取渠道

### 官方API平台
- **控制台**: https://platform.xiaomimimo.com
- **API端点**: https://token-plan-cn.xiaomimimo.com/v1 (OpenAI) / /anthropic (Anthropic)
- **定价文档**: https://platform.xiaomimimo.com/static/docs/pricing.md
- **llms.txt索引**: https://platform.xiaomimimo.com/llms.txt (可用curl直接抓取，含全部文档链接)

### 国内定价（元/1M tokens, 2026-05确认）

| 模型 | Input(Cache Hit) | Input(Cache Miss) | Output | 备注 |
|------|:-:|:-:|:-:|------|
| mimo-v2.5-pro / mimo-v2-pro | ¥1.40 | ¥7.00 | ¥21.00 | ≤256K上下文 |
| mimo-v2.5 | ¥0.56 | ¥2.80 | ¥14.00 | ≤256K |
| mimo-v2-omni | ¥0.56 | ¥2.80 | ¥14.00 | ≤256K |
| mimo-v2-flash | ¥0.07 | ¥0.70 | ¥2.10 | ≤256K |
| mimo-v2-tts / mimo-v2.5-tts / voiceclone / voicedesign | **限时免费** | — | — | Token计费，非按次 |

> 超过256K上下文时价格翻倍（如pro: Input Miss ¥14.00, Output ¥42.00）

### ⚠️ TTS计费说明
- TTS系列(mimo-v2-tts, mimo-v2.5-tts, mimo-v2.5-tts-voiceclone, mimo-v2.5-tts-voicedesign)
- 官方标注**"Limited-time free"**，按token计费（非按次收费）
- 上下文长度: 8K, 最大输出: 8K
- RPM: 100, TPM: 10M

### 文档发现方法
MiMo官方平台的完整文档可通过 `llms.txt` 索引文件获取:
```bash
curl -sL https://platform.xiaomimimo.com/llms.txt
# 包含: 定价、API文档、TTS使用指南、Token Plan说明、集成配置等
```

### 中转站参考
- api.tokex.top — 已知MiMo中转站，但会在上游成本上加价

### 降成本策略
1. **新模型内测期**: MiMo新模型发布时常有免费/优惠额度
2. **Token Plan批量**: 预付费套餐通常比按量便宜
3. **Cache Hit**: 利用缓存命中降低输入成本（Cache Hit价格约为Miss的20%）
4. **夜间使用**: 北京时间0:00-8:00消耗×0.8，等于多25%额度
5. **首购88折+邀请码9折叠加**: 新账号可拿到更低价格

### ⚠️ Token Plan套餐档位与Credits体系

Token Plan用统一Credits计量，不同模型按倍率扣减（不是直接扣token）。

| 档位 | 月费 | Credits/月 | 约Pro模型输出token |
|------|------|-----------|------------------|
| Lite | ¥39 | 41亿 | ~680万 |
| Standard | ¥99 | 110亿 | ~1,830万 |
| Pro | ¥329 | 380亿 | ~6,330万 |
| Max | ¥659 | 820亿 | ~1.37亿 |

四档模型权限完全相同，区别仅在Credits额度。Lite也能调mimo-v2.5-pro，只是消耗更快。

**Credits ≠ Tokens**：论坛/闲鱼说的"百亿token"实际是Credits。Standard的110亿Credits用Pro模型约=1.8亿token。

详细Credits消耗倍率和优惠体系见:
`references/mimo-official-pricing.md`

### ⚠️ V2系列已下线
MiMo-V2系列（mimo-v2-pro, mimo-v2-omni, mimo-v2-tts等）已于2026-06-30正式下线，请切到V2.5系列。

完整的三大平台（DeepSeek/Qwen/MiMo）定价对比见:
`new-api-deployment-antokex/references/upstream-pricing-2026-05.md`
