---
name: task-completion-protocol
description: 任务完成后的清理协议。防止已完成的任务在新session中被重复执行。每次任务完成时必须执行。
triggers:
  - 任务标记为completed
  - 用户说"完成了""搞定""done"
  - 一个阶段性工作结束
---

# 任务完成清理协议

## 问题
已完成的任务残留在todo中，新session看到后会重复执行。这是个严重bug。

## 必须执行的步骤（按顺序）

### 1. 更新记忆（memory工具）
- 将任务最终状态写入memory，格式：`【任务名-状态】关键结论/产出`
- 包含：文件路径、版本号、关键数据（如字数、检测结果）
- 如果任务有产出物，记录路径和版本

### 2. 清理todo
- 将完成的task标记status=completed
- **立即删除**已完成的task（todo merge删除或替换为空列表）
- 确保todo中只保留**当前活跃**的任务

### 3. 写入日志（如daily-log-manager技能可用）
- 记录任务完成时间、关键产出、下一步建议

### 4. 更新memory中的"当前活跃任务"
- 从活跃任务列表中移除已完成的
- 添加新发现的待办（如有）

## 检查清单（每次session开始时）
- [ ] 检查todo列表，是否有标记completed但未删除的task
- [ ] 检查memory中"当前活跃任务"是否与todo一致
- [ ] 如果不一致，以memory为准，清理todo残留

## 反面模式（绝对不要做）
- ❌ 看到completed的todo就去重新执行
- ❌ 不更新memory就结束任务
- ❌ 在todo里保留已完成的任务
- ❌ 新session不检查memory就开始工作
