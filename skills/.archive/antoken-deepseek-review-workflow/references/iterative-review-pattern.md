# 迭代审查模式（2026-07-05 Antoken 商用就绪）

## 审查流程

### 第1轮：全面审查
- 前端分 4 个模块审查
- 后端审查
- 账号系统审查
- 发现 12+ 个问题

### 第2轮：修复后重新审查
- 修复所有 P0 问题
- 重新生成模块文件
- 发送给 DeepSeek 验证
- 发现 3-5 个残留问题

### 第3轮：残留修复
- 修复所有残留问题
- 重新生成模块文件
- 发送给 DeepSeek 验证
- 发现 1-2 个遗漏

### 第4轮：最终确认
- 修复最后遗漏
- DeepSeek 确认"已通过"
- 进入下一个模块

## 典型残留问题

### 模块3（节点组件）残留
1. composite-node 仍订阅全局 nodesAtom/edgesAtom
2. video-node 按钮 hover 仍为蓝色
3. text-node 无用导入未清理
4. 空 <input /> 标签未移除

### 模块4（Canvas/UI）残留
1. config.assetUrl 仍在 createAssetNode 中写入
2. as NodeData 断言未完全移除
3. 未使用的 cfg 变量未删除

### 模块5（后端）残留
1. config.py 启动校验仍为 logger.warning
2. upload.py 缺少 logging 导入
3. stripe_routes.py 异常细节仍泄露

## 关键教训

1. **不能跳过迭代**：必须等 DeepSeek 确认后才能进入下一个模块
2. **必须提供代码**：修改后必须生成最新模块文件给阿戴
3. **必须验证修改**：用 search_files 确认修改确实生效
4. **必须运行测试**：npm run build + npm test 都必须通过
