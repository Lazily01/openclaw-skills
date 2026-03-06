---
name: agent-reach
description: 给 AI Agent "眼睛"，让它能看到整个互联网。支持搜索、读网页、提取字幕、读 RSS 等。
---

# Agent Reach Skills

让 Claw 具备互联网内容获取能力。

## 已安装组件

| 组件 | 状态 | 用途 |
|------|------|------|
| **agent-reach** | ✅ 已安装 | 诊断工具 |
| **mcporter** | ✅ 已安装 | MCP 客户端 |
| **bird CLI** | ✅ 已安装 | Twitter 工具（未配置 Cookie） |
| **yt-dlp** | ✅ 已安装 | YouTube/B站字幕提取 |
| **Exa 搜索** | ✅ 已配置 | 全网语义搜索 |

## 可用功能（5/12）

### ✅ 全网语义搜索
```bash
mcporter call exa.web_search_exa query:"搜索内容" numResults:5
```

### ✅ 读网页
```bash
curl -s "https://r.jina.ai/<URL>"
```

### ✅ 读 RSS
```python
import feedparser
feed = feedparser.parse("<RSS_URL>")
```

### ⚠️ YouTube/B站字幕
```bash
# 可能需要代理
yt-dlp --no-check-certificate --skip-download --write-auto-sub --sub-lang en --output "/tmp/test" "<URL>"
```

### ⚠️ Twitter
需要配置 Cookie：
```bash
agent-reach configure twitter-cookies "auth_token=xxx; ct0=yyy"
```

### ❌ 小红书
需要 Docker（未安装）

## 常用命令

### 诊断状态
```bash
agent-reach doctor
```

### 搜索示例
```bash
# 搜索 Web
mcporter call exa.web_search_exa query:"AI agent" numResults:5

# 搜索 Reddit（通过 Exa）
mcporter call exa.web_search_exa query:"site:reddit.com 话题" numResults:5

# 搜索 GitHub（通过 Exa）
mcporter call exa.web_search_exa query:"site:github.com 项目名" numResults:5
```

### 读网页示例
```bash
# 读取任意网页
curl -s "https://r.jina.ai/https://example.com"

# 读取 GitHub 仓库
curl -s "https://r.jina.ai/https://github.com/user/repo"
```

## 待配置

1. **gh CLI** - 需要 sudo 权限安装
2. **Twitter Cookie** - 需要用户从浏览器导出
3. **Docker** - 小红书 MCP 需要
4. **代理** - Reddit/B站服务器访问可能需要

---

*最后更新: 2026-02-27*
