---
name: reverse-skill-router
description: "18.7K星安全技能路由包 — 41条规则×42模块，覆盖APK/二进制/JS/CTF/渗透/恶意软件/固件/IoT/LLM安全/攻击链。AI自动路由+工具自举+经验进化。"
version: 1.0.0
author: zhaoxuya520 + 小黑
license: MIT
metadata:
  hermes:
    tags: [reverse-engineering, pentest, security, routing, ctf, malware, exploit]
    related_skills: [re-toolkit-mcp, godmode, ai-pentest-toolkit, pentest-pipeline, vulnclaw]
---

# reverse-skill — 安全技能路由包 (18.7K⭐)

**源码:** ~/security-research/re-tools/reverse-skill/
**GitHub:** https://github.com/zhaoxuya520/reverse-skill

## 核心能力

| 指标 | 数值 |
|------|------|
| 路由规则 | 41条 (R0-R40) |
| Skill模块 | 42个 |
| 回归测试 | 163个用例 |
| CI平台 | Windows + Ubuntu |

## 42个覆盖场景

```
APK/Android逆向     → skills/apk-reverse/
iOS/IPA逆向         → skills/mobile-reverse/
JS签名/前端加密     → skills/js-reverse/
.NET/dnSpy          → skills/dotnet-reverse/
二进制逆向(exe/dll/so/elf) → skills/ida-reverse/ + skills/radare2/
Ghidra逆向          → skills/ghidra-reverse/
Go/Rust逆向         → skills/go-rust-reverse/
CTF竞赛             → CTF-Sandbox-Orchestrator/ (42子skill)
渗透测试            → skills/pentest-tools/
恶意软件/YARA       → skills/malware-analysis/
固件/IoT            → skills/firmware-pentest/
LLM/AI安全          → skills/llm-security/
攻击链/红队         → skills/attack-chain/
浏览器自动化        → skills/browser-automation/
浏览器扩展逆向      → skills/browser-extension-reverse/
API安全             → skills/api-security/
数据库安全          → skills/database-security/
云/K8s安全          → skills/cloud-k8s/
代码审计            → skills/code-audit/
数字取证            → skills/digital-forensics/
EDR绕过             → skills/edr-bypass-re/
邮件安全            → skills/email-security/
身份联邦            → skills/identity-federation/
硬件安全            → skills/hardware-security/
二进制diff          → skills/binary-diff/
```

## 路由流程

```
用户任务 → MASTER-ROUTING.md (快速路由)
    │
    ├─ 命中 → PRIMARY skill → SKILL.md → 执行
    │
    └─ 歧义 → routing.md 全矩阵(三轴：目标类型/意图/工具链)
         │
         └─ 仍未命中 → 提议新skill
```

## 使用方式

### 方式1: 自动路由（推荐）
```bash
# 小黑自动根据用户消息选择对应skill
# "分析这个APK的加密" → 自动加载apk-reverse
# "逆向这个.so文件" → 自动加载ida-reverse + radare2
```

### 方式2: 路由脚本
```bash
# macOS版（需要转换PowerShell脚本）
python3 ~/security-research/re-tools/reverse-skill/skills/config/routing.json
```

### 方式3: 手动加载
```bash
# 直接读取对应skill的SKILL.md
skill_view(name="reverse-skill-router", file_path="references/routing.json")
```

## 路由规则速查 (TOP 10)

| ID | 条件 | PRIMARY |
|----|------|---------|
| R1 | APK/smali/jadx/apktool | apk-reverse |
| R2 | IPA/iOS/Objection/MobSF | mobile-reverse |
| R3 | JS签名/前端加密/jshook/CDP | js-reverse |
| R4 | DSL VM/fireye/自定义opcode | dsl-vm-reverse |
| R5 | .NET/dnSpy/de4dot/ConfuserEx | dotnet-reverse |
| R6 | exe/dll/so/elf/IDA/Ghidra | ida-reverse |
| R7 | CTF/flag/pwn/crypto/reverse | CTF-Sandbox |
| R8 | burp/nmap/sqlmap/xss/sqli | pentest-tools |
| R9 | malware/yara/sandbox/样本 | malware-analysis |
| R10 | firmware/iot/binwalk/uart | firmware-pentest |

## 授权门禁（硬性规则）

对任何目标动手前必须：
1. case-init 生成 scope.md
2. auth.status = granted
3. network_profile 就绪
4. **未授权禁止ACT**

## 与Hermes集成

本skill作为安全任务的**第一入口**。当用户消息命中安全/逆向关键词时：
1. 先读 MASTER-ROUTING.md 确定PRIMARY
2. 加载对应skill模块的SKILL.md
3. 按skill指令执行
4. 追加timeline/evidence
5. 输出Finding→Path报告

## 常见Pitfalls

- **PowerShell脚本需转换** — 原版是Windows PowerShell，macOS需要用bash/python重写
- **工具路径只认tool-index** — 首次运行需执行refresh-tool-index
- **case-init是必须的** — 不能跳过授权直接动手
- **routing.json是唯一真相源** — 改路由只改这个文件
