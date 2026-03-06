# Claw's Skills Library

个人技能库，包含 13 个 Skills。

## 分类

### 🔧 工具类 (Tools)

| Skill | 功能 | 触发词 |
|-------|------|--------|
| [agent-reach](./agent-reach) | 网络信息获取（搜索、网页、RSS） | "搜索"、"读网页"、"获取字幕" |
| [tavily-search](./tavily-search) | AI 优化搜索（Tavily API） | "搜索" |
| [obsidian-cli](./obsidian-cli) | Obsidian 笔记操作 | "写入 Obsidian"、"归档到笔记" |
| [file-organizer](./file-organizer) | 文件智能整理 | "整理文件"、"清理重复" |
| [find-skills](./find-skills) | 技能发现与安装 | "有什么技能"、"找技能" |

### 🎨 内容类 (Content)

| Skill | 功能 | 触发词 |
|-------|------|--------|
| [ai-image-generation](./ai-image-generation) | AI 生图（50+ 模型：FLUX, Gemini, Grok, Seedream） | "生成图片"、"flux" |
| [doubao-image-generation](./doubao-image-generation) | 豆包 AI 生图（2K-4K，去水印） | "豆包生图"、"画个图" |
| [podcast-skill](./podcast-skill) | 文本转播客音频（edge-tts） | "生成播客"、"朗读" |
| [twitter-reader](./twitter-reader) | Twitter/X 帖子读取 | "读这条推文" |

### 🤝 协作类 (Workflow)

| Skill | 功能 | 触发词 |
|-------|------|--------|
| [multi-agent-workflow](./multi-agent-workflow) | 多 Agent 协作指南 | PM/Dev/QA/Growth 协作 |
| [proactive-agent](./proactive-agent) | 主动 Agent 模式 | WAL、Working Buffer |

### 💼 业务类 (Business)

| Skill | 功能 | 触发词 |
|-------|------|--------|
| [hr-skill](./hr-skill) | 简历智能筛选 | "筛选简历"、"候选人匹配" |
| [monitor-skill](./monitor-skill) | 网页监控检查 | "监控网页"、"检查网站" |

## 统计

- **总计：** 13 个 Skills
- **工具类：** 5 个
- **内容类：** 4 个
- **协作类：** 2 个
- **业务类：** 2 个

## 安装

```bash
# 克隆仓库
git clone git@github.com:Lazily01/openclaw-skills.git

# 复制到 OpenClaw skills 目录
cp -r openclaw-skills/* ~/.openclaw/workspace/skills/
```

## 更新日志

### 2026-03-06
- 恢复 ai-image-generation（通用 AI 生图，50+ 模型）
- 恢复 tavily-search（AI 优化搜索）
- 新增 hr-skill（简历筛选）
- 新增 monitor-skill（网页监控）
- 新增 podcast-skill（播客生成）
- 新增 agent-reach（网络信息获取）
- 新增 obsidian-cli（Obsidian 操作）
- 新增 doubao-image-generation（豆包生图）
- 分类整理：工具/内容/协作/业务

---

*Created by Claw | Last updated: 2026-03-06*
