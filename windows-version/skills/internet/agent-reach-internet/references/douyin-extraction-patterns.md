# 抖音(Douyin)内容提取实战指南

## 已知限制（2026-07实测）

### 用户主页访问
- **登录墙**: 用户主页强制弹出登录弹窗，未登录无法查看视频列表
- **服务异常**: 视频列表区域显示"服务异常，重新刷新拉取数据"，即使关闭登录弹窗也无法加载
- **验证码中间页**: 搜索页面会触发验证码中间页
- **Bot检测**: 自动化访问会被检测，curl直接请求超时或返回空

### B站(Bilibili)访问
- **风控校验**: 错误码-352，UPINFO_ERROR: 风控校验失败
- **登录要求**: 视频列表需要登录才能查看

## 成功的替代方案

### 方案1: Web搜索（推荐）
```
web_search(query="创作者名 抖音 视频教程", limit=10)
```
- 可以找到视频标题、描述、发布时间
- 可以找到创作者的其他平台账号（B站、YouTube等）
- 可以找到视频的具体内容摘要

### 方案2: 从视频页面提取播放列表
当能访问单个视频页面时，用browser_console提取播放列表：
```javascript
const links = document.querySelectorAll('a[href*="/video/"]');
const videoLinks = [];
links.forEach(link => {
  const text = link.textContent.trim();
  const href = link.href;
  if (text && text.length > 5) {
    videoLinks.push({ text, href });
  }
});
videoLinks;
```
- 返回所有视频链接和标题
- 包含播放列表/合集信息

### 方案3: 提取章节要点
抖音视频页面有"章节要点"区域，包含视频内容摘要：
```javascript
// 查找章节要点区域
const keypoints = document.querySelector('[class*="chapter"], [class*="keypoint"]');
```

## 抖音用户信息提取
即使有登录墙，以下信息仍可从页面提取：
- 用户名、头像
- 关注数、粉丝数、获赞数
- 抖音号、IP属地、年龄
- 个人简介
- 作品数量

## 提取步骤（推荐流程）

1. **先用web_search搜索创作者**
   - 搜索"创作者名 抖音 视频教程"
   - 获取视频标题列表和内容摘要
   - 找到创作者的其他平台账号

2. **尝试访问单个视频页面**
   - 用browser_navigate访问具体视频URL
   - 用browser_console提取播放列表
   - 提取章节要点和内容摘要

3. **如需完整视频列表**
   - 搜索"创作者名 合集 系列教程"
   - 查找是否有整理好的视频合集页面

## 常见创作者类型

### AI编程类
- 关键词: Vibe Coding, Cursor, Claude Code, Codex, AI编程
- 内容: 工具教程、实战演示、工作流分享
- 平台: 抖音、B站、YouTube

### 技术教程类
- 关键词: 前端、后端、全栈、部署
- 内容: 从零到一教程、项目实战
- 平台: B站（更完整）、抖音（短视频摘要）

## 注意事项
- 抖音视频通常是短视频（1-15分钟），内容精炼
- 完整教程通常在B站或YouTube
- 搜索时加上"合集"、"系列"、"教程"等关键词效果更好
- 创作者通常会在多个平台发布内容，B站更容易访问
