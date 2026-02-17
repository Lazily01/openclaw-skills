# 🛠️ OpenClaw Skills 库

> 张老板的 Agent Skills 收藏

---

## 📚 当前 Skills

### Project Skills（项目级）

#### 1. find-skills 🔍

**功能：** 帮助发现和安装 agent skills

**用途：**
- 搜索现有 skills（`npx skills find <query>`）
- 安装新 skills（`npx skills add <package>`）
- 检查更新（`npx skills check`）

**技能来源：** https://skills.sh/

---

#### 2. tavily-search 🔎

**功能：** AI 优化的网络搜索（Tavily API）

**用途：**
- 网络搜索（返回简洁、相关的内容）
- URL 内容提取
- 新闻搜索
- 深度研究模式

**API Key：** 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

---

#### 3. proactive-agent 🦞

**功能：** 将 AI agent 从任务跟随者转变为主动合作伙伴

**版本：** v3.1.0

**核心特性：**

#### 三大支柱
- **Proactive（主动）** - 预测需求，无需询问
- **Persistent（持久）** - WAL Protocol、Working Buffer、上下文压缩恢复
- **Self-Improving（自改进）** - 自愈、 relentless resourcefulness

#### 核心协议
- **WAL Protocol** - Write-Ahead Logging，响应前记录重要信息
- **Working Buffer** - 危险区记录交换内容
- **Compaction Recovery** - 上下文丢失后逐步恢复
- **Heartbeat System** - 定期健康检查

**作者：** Hal Labs (Part of the Hal Stack)

---

### Global Skills（全局）

#### 4. ai-image-generation 🎨

**功能：** AI 图片生成（FLUX、Gemini、Grok 等 50+ 模型）

**用途：**
- 文本生图（Text-to-Image）
- 图像处理（Inpainting、Upscaling）
- 图片编辑

**模型：** FLUX Dev LoRA、FLUX.2 Klein LoRA、Gemini 3 Pro Image、Grok Imagine、Seedream 4.5、Reve 等

---

#### 5. file-organizer 📁

**功能：** 智能整理文件和文件夹

**用途：**
- 理解上下文，自动组织
- 查找重复文件
- 建议更好的组织结构

---

#### 6. multi-agent-workflow 🤖

**功能：** 多 Agent 协作工作流指南

**用途：**
- 协调 PM、Frontend、Backend、Mobile、QA Agent
- 复杂项目管理
- CLI 工作流

---

#### 7. twitter-reader 🐦

**功能：** 获取 Twitter/X 帖子内容

**用途：**
- 通过 jina.ai API 获取推文（绕过 JS 限制）
- 支持单个帖子或批量获取
- 获取作者、时间戳、文本、图片、回复

---

### Skills 总计：7 个
- Project Skills: 3 个
- Global Skills: 4 个

---

## 📁 目录结构

```
skills/
├── find-skills/              # Skills 发现工具（Project）
├── tavily-search/             # AI 优化的搜索（Project）
├── proactive-agent/           # 主动 agent 架构（Project）
├── ai-image-generation/       # AI 图片生成（Global）
├── file-organizer/           # 文件智能整理（Global）
├── multi-agent-workflow/      # 多 Agent 协作（Global）
└── twitter-reader/            # Twitter/X 帖子读取（Global）
```

---

## 🚀 使用方法

### 安装新 Skill

```bash
npx skills find <query>      # 搜索 skill
npx skills add <package>     # 安装 skill
```

### 更新所有 Skills

```bash
npx skills update
```

---

## ⚙️ 配置

### Tavily Search

需要设置环境变量：
```bash
export TAVILY_API_KEY="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"
```

---

## 📝 维护说明

### 添加新 Skill

1. 将 skill 放到 `skills/` 目录下
2. 提交并推送到 GitHub
3. 在本 README 中添加说明

### 更新 Skill

1. 修改 skill 文件
2. 提交并推送
3. 更新 README 中的版本信息

### 删除 Skill

1. 删除 skill 目录
2. 提交并推送
3. 从 README 中移除说明

---

## 🔗 相关资源

- [OpenClaw 文档](https://docs.openclaw.ai)
- [Skills Hub](https://skills.sh/)
- [Proactive Agent 文档](https://github.com/openclaw/skills/tree/main/proactive-agent)

---

**维护者：** 张老板 (Lazily01)
**最后更新：** 2026-02-17
