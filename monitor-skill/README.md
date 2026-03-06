# Monitor Skill - 网页监控检查

网页监控与检查工具，支持可用性检测、价格提取、关键词检测、内容变化追踪。

## 快速使用

### 在 OpenClaw 中使用（推荐）

直接对我说：
- "帮我检查这个网站能访问吗"
- "这个商品多少钱"
- "这个网页有'降价'关键词吗"
- "帮我监控这个网页内容变化"

### 命令行使用

```bash
# 可用性检查
python3 scripts/monitor.py --url https://github.com --check availability

# 价格检查
python3 scripts/monitor.py --url https://item.jd.com/xxx --check price

# 价格监控（设置目标价格）
python3 scripts/monitor.py --url https://item.jd.com/xxx --check price --threshold 100

# 关键词检测
python3 scripts/monitor.py --url https://example.com --check keyword --keywords "降价,促销"

# 内容变化检测
python3 scripts/monitor.py --url https://example.com --check content

# 全面检查
python3 scripts/monitor.py --url https://example.com --check all
```

## 功能

| 功能 | 说明 |
|------|------|
| 🌐 可用性检测 | 检查网站是否可访问、响应时间、HTTP 状态码 |
| 💰 价格提取 | 从网页提取商品价格 |
| 🔍 关键词检测 | 检测关键词是否出现、出现次数 |
| 📄 内容变化 | 追踪网页内容是否变化 |
| 📊 报告生成 | 输出检查报告 |

## 使用场景

### 1. 检查网站是否正常
```bash
python3 scripts/monitor.py --url https://github.com --check availability
```

### 2. 监控商品价格
```bash
# 检查当前价格
python3 scripts/monitor.py --url https://item.jd.com/xxx --check price

# 设置目标价格，价格达标时提醒
python3 scripts/monitor.py --url https://item.jd.com/xxx --check price --threshold 199
```

### 3. 检测关键词
```bash
python3 scripts/monitor.py --url https://news.example.com --check keyword --keywords "AI,GPT,ChatGPT"
```

### 4. 监控内容变化
```bash
# 首次运行会记录内容哈希
python3 scripts/monitor.py --url https://example.com --check content

# 再次运行会对比内容是否变化
python3 scripts/monitor.py --url https://example.com --check content
```

## 配置

无需特殊配置，开箱即用。

可选配置 `~/.monitor-skill/config.json`：

```json
{
  "timeout": 30,
  "user_agent": "Mozilla/5.0 ..."
}
```

## 输出示例

```markdown
# 网页检查报告

**URL:** https://example.com/product
**时间:** 2026-03-06 15:45:00

## 🌐 可用性

| 检查项 | 结果 |
|--------|------|
| 状态 | ✅ 正常 |
| HTTP 状态码 | 200 |
| 响应时间 | 150ms |
| 速度评级 | 优秀 |

## 💰 价格

| 检查项 | 结果 |
|--------|------|
| 当前价格 | ¥199.00 |
| 目标价格 | ¥150 |
| 是否达标 | ❌ 否 |
```

## 注意事项

- 某些网站需要登录才能访问内容
- 价格提取依赖网页结构，不同网站效果可能不同
- 内容变化检测基于哈希对比，只能检测文本变化

---

*Created: 2026-03-06*
