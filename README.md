# Claw's Skills Library

个人技能库，包含 26 个 Skills。

## 分类

### 🔧 工具类 (Tools)

| Skill | 功能 | 来源 |
|-------|------|------|
| [agent-reach](./agent-reach) | 网络信息获取（搜索、网页、RSS、YouTube、小红书等） | [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) |
| [tavily-search](./tavily-search) | AI 优化搜索（Tavily API） | Clawhub |
| [obsidian-cli](./obsidian-cli) | Obsidian 笔记操作 | Clawhub |
| [file-organizer](./file-organizer) | 文件智能整理 | Clawhub |
| [find-skills](./find-skills) | 技能发现与安装 | Clawhub |
| [disk-cleaner](./disk-cleaner) | 磁盘清理工具 | Clawhub |
| [tinybird](./tinybird) | 数据分析平台 | [tinybirdco/tinybird-agent-skills](https://github.com/tinybirdco/tinybird-agent-skills) |

### 🎨 内容类 (Content)

| Skill | 功能 | 来源 |
|-------|------|------|
| [ai-image-generation](./ai-image-generation) | AI 生图（50+ 模型：FLUX, Gemini, Grok, Seedream） | [inference-sh/skills](https://github.com/inference-sh/skills) |
| [doubao-image-generation](./doubao-image-generation) | 豆包 AI 生图（2K-4K，去水印） | 原创 |
| [podcast-skill](./podcast-skill) | 文本转播客音频（edge-tts） | 原创 |
| [twitter-reader](./twitter-reader) | Twitter/X 帖子读取 | Clawhub |
| [bird](./bird) | Twitter/X CLI（读取、搜索、发推） | [steipete/bird](https://github.com/steipete/bird) |
| [xhs-note-creator](./xhs-note-creator) | 小红书笔记创作（内容+图片+发布） | 原创 |
| [frontend-design](./frontend-design) | 高质量前端界面设计 | Clawhub |

### 🤝 协作类 (Workflow)

| Skill | 功能 | 来源 |
|-------|------|------|
| [multi-agent-workflow](./multi-agent-workflow) | 多 Agent 协作指南 | Clawhub |
| [proactive-agent](./proactive-agent) | 主动 Agent 模式（WAL、Working Buffer） | [halthelobster/proactive-agent](https://github.com/halthelobster/proactive-agent) |
| [pm-agent](./pm-agent) | 产品经理（需求分解、任务规划） | 原创 |
| [deep-research](./deep-research) | 深度调研（8 阶段研究流程） | [199-biotechnologies/claude-deep-research-skill](https://github.com/199-biotechnologies/claude-deep-research-skill) |

### 💻 开发类 (Development)

| Skill | 功能 | 来源 |
|-------|------|------|
| [code-simplifier](./code-simplifier) | 代码简化重构 | Anthropic |
| [fullstack-developer](./fullstack-developer) | 全栈开发（React, Node.js, 数据库） | awesome-llm-apps |
| [e2e-testing-patterns](./e2e-testing-patterns) | E2E 测试（Playwright, Cypress） | Clawhub |
| [webapp-testing](./webapp-testing) | Web 应用测试工具包 | Clawhub |

### 💼 业务类 (Business)

| Skill | 功能 | 来源 |
|-------|------|------|
| [hr-skill](./hr-skill) | 简历智能筛选 | 原创 |
| [monitor-skill](./monitor-skill) | 网页监控检查 | 原创 |
| [developer-growth-analysis](./developer-growth-analysis) | 开发者成长分析 | Clawhub |
| [postbridge-social-growth](./postbridge-social-growth) | 社交媒体增长策略（TikTok/Instagram） | Clawhub |

## 统计

- **总计：** 26 个 Skills
- **工具类：** 7 个
- **内容类：** 7 个
- **协作类：** 4 个
- **开发类：** 4 个
- **业务类：** 4 个

## 原创 vs 第三方

| 类型 | 数量 | Skills |
|------|------|--------|
| 原创 | 5 个 | doubao-image-generation, podcast-skill, xhs-note-creator, pm-agent, hr-skill, monitor-skill |
| 第三方 | 21 个 | 其余均为社区/官方 skills |

## 安装

```bash
# 克隆仓库
git clone git@github.com:Lazily01/openclaw-skills.git

# 复制到 OpenClaw skills 目录
cp -r openclaw-skills/* ~/.openclaw/workspace/skills/
```

## 更新日志

### 2026-03-06
- 整合所有 Agent 专属 skills 到主库
- 新增全局 skills（deep-research, disk-cleaner, tinybird）
- 新增 PM Agent skill（pm-agent）
- 新增开发类 skills（code-simplifier, frontend-design, fullstack-developer, e2e-testing-patterns, webapp-testing）
- 新增业务类 skills（developer-growth-analysis, postbridge-social-growth）
- Skills 总计：26 个
- 分类：工具/内容/协作/开发/业务

---

*Created by Claw | Last updated: 2026-03-06*
