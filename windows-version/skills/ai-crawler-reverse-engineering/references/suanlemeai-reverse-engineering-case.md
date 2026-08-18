# suanlemeai.cn 逆向工程实战记录

> 日期：2026-07-08
> 目标：逆向算命网站 suanlemeai.cn 并搭建本地测试环境

## 背景

用户要求逆向 suanlemeai.cn（算了么 - 东方命理推演云台）的所有代码，搭建本地测试网站。
用户明确要求："完全真实逆向，不要自己编"、"需要帮助就去GitHub找，不要来问我"。

## 执行过程

### Phase 1: 侦察

**问题：browser_navigate 3次超时**
- 第1次：`browser_navigate("https://suanlemeai.com")` → SSL错误（域名不对，应该是.cn）
- 第2次：`browser_navigate("http://suanlemeai.com")` → ERR_BLOCKED_BY_CLIENT
- 第3次：`browser_navigate("https://suanlemeai.cn/")` → 超时
- 第4次：`browser_navigate("https://suanlemeai.cn/tools")` → 超时
- 第5次：`browser_navigate("https://suanlemeai.cn/tools/bazi")` → 超时

**解决方案：web_extract + web_search 组合**
```python
# 获取页面内容
web_extract(urls=["https://suanlemeai.cn/", "https://suanlemeai.cn/tools"])

# 搜索技术栈信息
web_search(query="suanlemeai.cn 技术栈")
web_search(query="suanlemeai next.js react vue")
web_search(query="suanlemeai github")

# 搜索开源项目
web_search(query="算命网站 开源")
web_search(query="八字排盘 开源")
web_search(query="紫微斗数 github")
```

### Phase 2: 深度分析

**Subagent 1: 技术栈分析**
- 输入：web_search + web_extract 结果
- 输出：/tmp/suanlemeai-reverse-engineering.md（25,477字节）
- 发现：SPA架构、客户端计算、27个工具、会员系统

**Subagent 2: GitHub开源项目搜索**
- 输入：10+个搜索关键词
- 输出：/tmp/suanlemeai-deep-analysis.md（19,274字节）
- 发现：iztro（紫微，3.9k stars）、lunar-javascript（八字，1.6k stars）、jishiyu（功能最全）、mingyu（最佳API）

### Phase 3: 代码搭建

**Subagent 3: 本地测试环境**
- 基于天机阁项目（/Users/macpro/tianji-ge）
- 安装 iztro + lunar-javascript 依赖
- 创建4个核心排盘页面：八字、紫微、梅花易数、奇门遁甲
- 输出：setup-and-run.sh 启动脚本

## 关键发现

1. **suanlemeai.cn 技术栈**：Next.js/React + TypeScript + Tailwind CSS，客户端计算优先
2. **必用开源库**：iztro（紫微斗数）、lunar-javascript（农历/八字）
3. **最佳参考项目**：jishiyu（功能最全）、mingyu（最佳API）、MingPan（纯引擎）
4. **架构模式**：入局概念、档案系统、会员分层、真太阳时

## 文件库创建流程

当用户要求"全部逆向回来放到桌面作为文件库"时，执行以下流程：

### 1. 创建目录结构
```bash
mkdir -p ~/Desktop/{网站名}-逆向文件库/{前端代码/{HTML,CSS,JS,组件},排盘算法/{各术数目录},API接口/{接口文档,示例代码},开源参考/{各项目目录},本地测试/{项目目录,测试页面}}
```

### 2. 批量提取页面HTML
**关键：用 execute_code 而不是 delegate_task**（delegate_task容易超时）

```python
from hermes_tools import web_extract, write_file

pages = [
    {"url": "https://example.com/", "filename": "index.html"},
    {"url": "https://example.com/tools", "filename": "tools.html"},
    # ... 更多页面
]

for page in pages:
    result = web_extract(urls=[page["url"]])
    if result and "results" in result:
        content = result["results"][0].get("content", "")
        if content:
            write_file(path=f"~/Desktop/逆向文件库/前端代码/HTML/{page['filename']}", content=content)
```

### 3. 提取GitHub开源项目README
```python
from hermes_tools import web_extract, write_file

# 提取README（注意路径：main 或 master）
readme_url = "https://raw.githubusercontent.com/用户名/仓库名/main/README.md"
result = web_extract(urls=[readme_url])
if result and "results" in result:
    content = result["results"][0].get("content", "")
    write_file(path="~/Desktop/逆向文件库/排盘算法/xxx/README.md", content=content)
```

### 4. 创建索引文档
每个目录都需要一个README.md索引文件，包括：
- 文件列表和说明
- 使用方法
- 参考资源

### 5. 创建总结文档
- 技术栈分析.md
- 逆向工程总结.md
- API接口文档.md

## 经验教训

1. **browser_navigate 超时时立即切换 web_extract**，不要反复重试
2. **批量提取用 execute_code**，不要用 delegate_task（容易超时）
3. **用户说"不要来问我"时**，所有决策由agent自行判断，参考GitHub开源项目
4. **"完全真实逆向"** = 用 web_extract 获取真实页面内容，用 web_search 获取真实项目信息，不编造数据
5. **"放到桌面作为文件库"** = 创建完整目录结构 + 索引文档 + 总结文档
6. **GitHub README提取** = 用 raw.githubusercontent.com/用户名/仓库名/main/README.md
7. **文件库结构** = 前端代码/HTML + 排盘算法 + API接口 + 开源参考 + 本地测试
