# HR Skill - 简历智能筛选

智能简历筛选工具，支持 LLM 解析、岗位匹配和邮箱获取。

## 快速使用

### 在 OpenClaw 中使用（推荐）

直接对我说：
- "帮我筛选这份简历"
- "这个候选人匹配运营总监吗"
- "从邮箱获取简历并筛选"

### 命令行使用

```bash
# 配置（首次）
python3 scripts/resume_screener.py --setup

# 添加岗位
python3 scripts/resume_screener.py --add-job

# 列出岗位
python3 scripts/resume_screener.py --list-jobs

# 筛选单个简历
python3 scripts/resume_screener.py --file resume.pdf --job 运营总监

# 批量筛选
python3 scripts/resume_screener.py --dir resumes/ --job 运营总监

# 从邮箱获取简历并筛选
python3 scripts/resume_screener.py --from-email --job 运营总监 --email-limit 50
```

## 功能

| 功能 | 说明 |
|------|------|
| 📄 简历解析 | 提取姓名、技能、经验、学历等 |
| 🎯 岗位匹配 | 计算匹配度、生成推荐指数 |
| 📊 智能排序 | 按推荐度排序候选人 |
| 📬 邮箱获取 | 从邮箱批量下载简历附件 |
| 📧 报告生成 | 输出筛选报告 |

## 岗位配置

### 添加岗位

```bash
python3 scripts/resume_screener.py --add-job
```

或手动创建 `jobs/岗位名.json`：

```json
{
  "title": "运营总监",
  "required_experience": 3,
  "required_education": "本科",
  "required_skills": ["运营管理", "团队管理", "数据分析"],
  "bonus_skills": ["互联网经验", "从0到1经验"],
  "description": "负责公司整体运营战略..."
}
```

## 邮箱配置

### 配置邮箱（首次）

```bash
python3 scripts/resume_screener.py --setup
```

按提示输入：
- 发件邮箱 + 授权码（用于发送报告）
- IMAP 邮箱 + 授权码（用于获取简历）

### 常见邮箱 IMAP 配置

| 邮箱 | IMAP 服务器 | 端口 |
|------|-------------|------|
| QQ 邮箱 | imap.qq.com | 993 |
| 163 邮箱 | imap.163.com | 993 |
| Gmail | imap.gmail.com | 993 |
| Outlook | outlook.office365.com | 993 |

## 两种运行模式

### 模式 1：AI 协作（推荐）

通过 OpenClaw 调用，AI 使用内置能力解析简历。

**优点：**
- 无需配置 API
- 解析效果更好
- 自动归档到 Obsidian

### 模式 2：独立运行

配置 LLM API 后，脚本独立运行：

```bash
# 配置 API
python3 scripts/resume_screener.py --setup

# 筛选简历
python3 scripts/resume_screener.py --file resume.pdf --job 运营总监
```

**支持的 API：**
- zai (智谱/GLM)
- openai
- anthropic

## 依赖

```bash
pip install pymupdf python-docx requests
```

## 配置文件

用户配置保存在：`~/.hr-skill/config.json`

```json
{
  "api_provider": "zai",
  "api_key": "your-api-key",
  "model": "glm-5",
  "email_sender": "",
  "email_password": "",
  "email_recipient": "",
  "imap_server": "imap.qq.com",
  "imap_port": 993,
  "imap_email": "",
  "imap_password": ""
}
```

## 输出示例

```markdown
# 简历筛选报告

**岗位：** 运营总监
**日期：** 2026-03-06
**处理数量：** 3 份

## ⭐⭐⭐⭐⭐ 强烈推荐

### 1. 吴芬 - 17年经验

- **匹配度：** 90%
- **技能：** 运营管理、团队管理、新媒体运营
- **推荐理由：** 推荐
```

---

*Updated: 2026-03-06*
