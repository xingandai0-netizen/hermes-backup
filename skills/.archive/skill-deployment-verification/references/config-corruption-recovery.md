# Config Corruption Recovery Procedure

## 情况：config.yaml被覆盖或截断

**症状：**
- system_prompt_append长度异常小（正常>10K，截断后可能<3K）
- skill路由丢失，新session不触发任何skill加载
- MCP servers段为空

**原因：**
- hermes config set写入失败或中途截断
- YAML解析错误导致回退到默认值
- 并发写入冲突

## 恢复步骤

### 1. 查找备份
```bash
# 检查自动备份（按时间排序）
ls -lt ~/.hermes/config.yaml.bak.* ~/.hermes/config.yaml.corrupt.* 2>/dev/null | head -10

# .corrupt文件通常是损坏前的完整版本
# .bak文件是hermes自动备份
```

### 2. 验证备份有效性
```bash
python3 -c "
import yaml
for f in ['config.yaml.corrupt.YYYYMMDD-HHMMSS.bak', 'config.yaml.bak.YYYYMMDD_HHMMSS']:
    try:
        with open(f'~/.hermes/{f}') as fh:
            c = yaml.safe_load(fh.read())
        spa = c.get('agent', {}).get('system_prompt_append', '')
        print(f'{f}: {len(spa)} chars - VALID')
    except Exception as e:
        print(f'{f}: PARSE ERROR - {e}')
"
```

### 3. 提取system_prompt_append（YAML损坏时）

如果整个文件YAML解析失败，用字符串方式提取：
```python
with open('~/.hermes/config.yaml.corrupt.xxx.bak') as f:
    raw = f.read()

# 找到system_prompt_append的值
start = raw.find('system_prompt_append: "') + len('system_prompt_append: "')
# 找到值结束位置（terminal:之前）
end_region = raw.find('\nterminal:', start)
segment = raw[start:end_region]
last_quote = segment.rfind('"')
value = segment[:last_quote]

# 反转义YAML双引号字符串
value = value.replace('\\\n    ', '').replace('\\\n', '')
value = value.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
```

### 4. 写回config.yaml
```python
# 用YAML literal block scalar（|）避免引号问题
yaml_spa = '  system_prompt_append: |\n'
for line in spa_content.split('\n'):
    yaml_spa += '    ' + line + '\n'
```

### 5. 验证恢复结果
```bash
python3 -c "
import yaml
with open('~/.hermes/config.yaml') as f:
    c = yaml.safe_load(f.read())
spa = c['agent']['system_prompt_append']
mcp = c.get('mcp_servers', {})
print(f'SPA: {len(spa)} chars')
print(f'G0DM0D3: {\"G0DM0D3\" in spa}')
print(f'NEXUS: {\"NEXUS\" in spa}')
print(f'MCP: {len(mcp)} servers')
print(f'tirith: {c.get(\"security\", {}).get(\"tirith_enabled\")}')
"
```

## Skill目录名不匹配修复

当skill路由引用的name与实际目录名不一致时：

```bash
# 1. 找到实际目录
find ~/.hermes/skills -name 'SKILL.md' -exec grep -l 'name: TARGET-NAME' {} \;

# 2. 重命名目录
mv ~/.hermes/skills/category/old-dir-name ~/.hermes/skills/category/TARGET-NAME

# 3. 同步所有引用（必须全部更新）
sed -i '' 's/old-dir-name/TARGET-NAME/g' ~/.hermes/skills/INTENT-ROUTES.md
sed -i '' 's/old-dir-name/TARGET-NAME/g' ~/.hermes/skills/SKILL-INDEX.md
sed -i '' 's/old-dir-name/TARGET-NAME/g' ~/.hermes/skills/INDEX.json
sed -i '' 's/old-dir-name/TARGET-NAME/g' ~/.hermes/skills/.usage.json
sed -i '' 's/old-dir-name/TARGET-NAME/g' ~/.hermes/config.yaml
```
