---
name: agent-reach-internet
description: >-
  Agent-Reach：给AI Agent装上互联网眼睛，支持读取和搜索Twitter、Reddit、YouTube、
  GitHub、Bilibili、小红书、微博、抖音、V2EX、雪球等15+平台，零API费用。
  当需要从社交媒体、视频平台、论坛获取信息时激活。
version: 1.4.0
author: Hermes Agent (基于 Panniantong/Agent-Reach)
activation: /internet
license: MIT
metadata:
  created: 2026-04-17
  sources:
    - https://github.com/Panniantong/Agent-Reach
    - https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
---

# /internet

Agent-Reach：给AI Agent一键装上互联网能力的CLI工具。

## 触发条件

当用户提到以下内容时激活：
- "帮我看看这个推文/微博/小红书"
- "搜索Twitter/Reddit/YouTube"
- "这个视频讲了什么"
- "帮我订阅RSS"
- "搜索GitHub仓库"
- "看看这个网页内容"
- "B站视频总结"

## 抖音/B站访问注意事项（2026-07实测）
- 抖音用户主页有强制登录墙，视频列表显示"服务异常"
- B站有风控校验（错误码-352），自动化访问会被拦截
- **推荐方案**: 用web_search搜索创作者内容，或从单个视频页面用browser_console提取播放列表
- 详见 `references/douyin-extraction-patterns.md`

## 核心特性

### 🌐 支持的平台（15+）

| 平台 | 类型 | 功能 |
|------|------|------|
| Twitter/X | 社交媒体 | 读取推文、搜索、用户信息 |
| Reddit | 论坛 | 帖子、评论、子版块搜索 |
| YouTube | 视频 | 字幕提取、视频信息 |
| Bilibili | 视频 | 视频信息、字幕 |
| 小红书 | 社交电商 | 笔记、搜索 |
| 微博 | 社交媒体 | 微博、用户信息 |
| 抖音 | 短视频 | 视频信息 |
| GitHub | 代码托管 | 仓库、Issue、PR、搜索 |
| V2EX | 技术论坛 | 帖子、评论 |
| 雪球 | 金融社区 | 股票讨论、资讯 |
| LinkedIn | 职业社交 | 动态、公司信息 |
| 小宇宙 | 播客 | 播客内容 |
| RSS | 订阅源 | RSS/Atom订阅 |
| Web | 网页 | 通用网页阅读 |
| Exa | 搜索引擎 | AI增强搜索 |

### 🔑 零API费用

- **无需付费API** - 使用官方CLI工具和爬虫技术
- **自动Cookie管理** - 支持从浏览器提取Cookie
- **智能环境检测** - 自动判断本地/服务器环境

## 安装

### 快速安装
```bash
# 使用pip安装
pip install agent-reach

# 或使用uv（推荐）
uv tool install agent-reach
```

### 环境检测
```bash
# 检测所有渠道状态
agent-reach doctor

# 安装所有依赖
agent-reach install --env=auto

# 完整设置向导
agent-reach setup
```

## CLI命令

### 基础命令
```bash
# 查看帮助
agent-reach --help

# 环境健康检查
agent-reach doctor

# 安装依赖
agent-reach install --env=auto

# 配置Cookie
agent-reach configure twitter-cookies "auth_token=xxx; ct0=yyy"
```

### 使用示例

#### 1. Twitter/X
```bash
# 读取推文
agent-reach twitter https://twitter.com/user/status/123456

# 搜索推文
agent-reach twitter-search "AI agent" --limit 10

# 用户信息
agent-reach twitter-user @username
```

#### 2. YouTube
```bash
# 获取视频字幕
agent-reach youtube https://www.youtube.com/watch?v=xxx

# 搜索视频
agent-reach youtube-search "python tutorial" --limit 5
```

#### 3. Reddit
```bash
# 读取帖子
agent-reach reddit https://reddit.com/r/python/post/xxx

# 搜索帖子
agent-reach reddit-search "machine learning" --subreddit python
```

#### 4. 小红书
```bash
# 读取笔记
agent-reach xiaohongshu https://www.xiaohongshu.com/explore/xxx

# 搜索笔记
agent-reach xiaohongshu-search "护肤品推荐" --limit 10
```

#### 5. GitHub
```bash
# 查看仓库
agent-reach github-repo owner/repo

# 搜索仓库
agent-reach github-search "LLM framework" --limit 10

# 查看Issue
agent-reach github-issue owner/repo 123
```

#### 6. 网页阅读
```bash
# 阅读任意网页
agent-reach web https://example.com/article

# 使用Jina Reader（更干净）
curl https://r.jina.ai/https://example.com
```

#### 7. RSS订阅
```bash
# 解析RSS
agent-reach rss https://example.com/feed.xml

# 监控RSS更新
agent-rss watch https://example.com/feed.xml --interval 3600
```

## 核心架构

### Channel系统
Agent-Reach采用Channel架构，每个平台是一个Channel：

```python
# Channel基类
class Channel(ABC):
    name: str = ""           # 平台名称，如 "youtube"
    description: str = ""    # 描述，如 "YouTube 视频和字幕"
    backends: List[str] = [] # 后端工具，如 ["yt-dlp"]
    tier: int = 0            # 配置等级：0=零配置, 1=需要免费key, 2=需要配置

    def can_handle(self, url: str) -> bool:
        """检查是否能处理该URL"""
    
    def check(self, config) -> Tuple[str, str]:
        """检查工具是否可用，返回 (状态, 消息)"""
```

### 已注册的Channels
| Channel | 后端工具 | Tier | 功能 |
|---------|----------|------|------|
| GitHubChannel | gh CLI | 0 | 仓库、Issue、PR、搜索 |
| TwitterChannel | twitter-cli | 1 | 推文、用户、搜索 |
| YouTubeChannel | yt-dlp | 0 | 视频信息、字幕 |
| RedditChannel | rdt-cli | 0 | 帖子、评论、搜索 |
| BilibiliChannel | yt-dlp + bili-cli | 1 | 视频、字幕、搜索 |
| XiaoHongShuChannel | xhs-cli | 1 | 笔记、搜索 |
| DouyinChannel | 抖音API | 1 | 视频信息 |
| LinkedInChannel | linkedin-api | 2 | 动态、公司信息 |
| WeChatChannel | 微信API | 2 | 公众号内容 |
| WeiboChannel | weibo-cli | 1 | 微博、用户 |
| XiaoyuzhouChannel | 小宇宙API | 0 | 播客内容 |
| V2EXChannel | v2ex-cli | 1 | 帖子、评论 |
| XueqiuChannel | xueqiu-cli | 1 | 股票讨论、资讯 |
| RSSChannel | feedparser | 0 | RSS/Atom订阅 |
| ExaSearchChannel | Exa API | 1 | AI增强搜索 |
| WebChannel | Jina Reader | 0 | 通用网页阅读 |

### 配置系统
配置存储在 `~/.agent-reach/config.yaml`：

```yaml
# Twitter配置
twitter_auth_token: "xxx"
twitter_ct0: "yyy"

# Exa搜索配置
exa_api_key: "your-key"

# B站代理（可选）
bilibili_proxy: "http://proxy:port"

# Groq Whisper配置
groq_api_key: "your-key"
```

### Doctor环境检测
```bash
# 检测所有渠道状态
agent-reach doctor

# 输出示例：
# ✅ GitHub: gh CLI 已认证
# ⚠️  Twitter: twitter-cli 已安装但未配置Cookie
# ❌ Reddit: rdt-cli 未安装
# ✅ YouTube: yt-dlp + Node.js runtime
# ✅ Web: Jina Reader 可用
```

## MCP集成

Agent-Reach支持MCP（Model Context Protocol），可与Claude Desktop等AI工具集成。

### 配置MCP
```json
{
  "mcpServers": {
    "agent-reach": {
      "command": "agent-reach",
      "args": ["mcp"]
    }
  }
}
```

### MCP工具
```python
# 通过MCP调用
{
  "name": "agent_reach_search",
  "arguments": {
    "platform": "twitter",
    "query": "AI agent",
    "limit": 10
  }
}
```

## Cookie配置

### Twitter Cookie
```bash
# 从浏览器提取
1. 打开Twitter网页版
2. F12打开开发者工具
3. Application → Cookies
4. 复制 auth_token 和 ct0

# 配置
agent-reach configure twitter-cookies "auth_token=xxx; ct0=yyy"
```

### 小红书Cookie
```bash
# 从小红书网页版提取
1. 登录小红书网页版
2. F12 → Network → 找任意请求
3. 复制Cookie头

# 配置
agent-reach configure xiaohongshu-cookies "a1=xxx; web_session=yyy"
```

## 实战场景

### 场景1：竞品监控
```bash
# 监控Twitter上竞品讨论
agent-reach twitter-search "竞品名称" --limit 20 > mentions.txt

# 监控Reddit讨论
agent-reach reddit-search "竞品名称" --subreddit technology > reddit_mentions.txt
```

### 场景2：技术学习
```bash
# 获取YouTube教程字幕
agent-reach youtube https://www.youtube.com/watch?v=xxx > transcript.txt

# 搜索GitHub开源项目
agent-reach github-search "awesome LLM" --limit 10
```

### 场景3：舆情分析
```bash
# 小红书产品口碑
agent-reach xiaohongshu-search "产品名称" --limit 20

# 微博热点追踪
agent-reach weibo-search "话题名称" --limit 20
```

### 场景4：内容监控
```bash
# RSS订阅更新
agent-rss watch https://techcrunch.com/feed/ --interval 3600

# GitHub仓库监控
agent-reach github-watch owner/repo --check-interval 1800
```

## 与原生工具对比

| 功能 | 原生方式 | Agent-Reach |
|------|----------|-------------|
| Twitter | 需要API Key付费 | 免费CLI |
| YouTube | 需要API Key | yt-dlp免费 |
| Reddit | API限制严格 | 免费CLI |
| 小红书 | 需要登录 | 自动Cookie |
| GitHub | gh CLI配置复杂 | 一键配置 |
| 网页 | HTML杂乱 | 清洁提取 |

## 故障排除

### Cookie过期
```bash
# 重新配置Cookie
agent-reach configure twitter-cookies "新cookie"

# 或清除旧Cookie
agent-reach configure --clear twitter-cookies
```

### 环境检测失败
```bash
# 手动安装Node.js依赖
npm install -g twitter-cli rdt-cli

# 手动安装Python依赖
pip install yt-dlp feedparser
```

### IP被封
```bash
# 使用代理
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port

# 或配置Cookie绕过
agent-reach configure --use-cookies
```

## 最佳实践

1. **定期更新** - `pip install --upgrade agent-reach`
2. **Cookie管理** - 定期刷新Cookie避免过期
3. **代理配置** - 在服务器环境配置代理
4. **缓存利用** - 启用本地缓存减少请求
5. **错误监控** - 使用`agent-reach doctor`定期检查

## 安装建议

```bash
# 推荐使用uv安装（更快）
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install agent-reach

# 验证安装
agent-reach --version
agent-reach doctor
```

---
*技能基于 Panniantong/Agent-Reach 仓库*
*支持平台: Twitter, Reddit, YouTube, Bilibili, 小红书, 微博, 抖音, GitHub, V2EX, 雪球, LinkedIn, 小宇宙, RSS, Web, Exa*
