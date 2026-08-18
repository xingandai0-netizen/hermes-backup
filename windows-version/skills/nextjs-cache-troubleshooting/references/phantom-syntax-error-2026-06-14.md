# 幻影语法错误案例 — 2026-06-14

## 症状
```
x Expected ',', got '}'
   ,-[/Users/macpro/antoken/frontend/src/components/nodes/CompositeNode.tsx:360:1]
 360 |     </BaseNode>
 361 |   );
 362 | }
 363 | });
     : ^
```

## 实际文件状态
- CompositeNode.tsx 第363行是空行（文件总共372行）
- 文件语法完全正确，没有多余的`});`
- 错误来自 `.next` 缓存中的旧版本

## 根因
多次代码修改后，`.next/cache/webpack/` 中保留了旧的编译结果。dev server的HMR（Hot Module Replacement）在增量编译时与缓存冲突，导致使用了旧版本的文件内容。

## 修复
```bash
lsof -ti:3000 | xargs kill -9 2>/dev/null
cd ~/antoken/frontend && rm -rf .next .swc
npm run dev
```

## 关键教训
- **不要假设编译报错 = 文件损坏**
- 先用 `read_file` 验证文件实际内容
- 如果文件正确但编译报错 → 清缓存
- 清缓存时同时清 `.next` 和 `.swc`
