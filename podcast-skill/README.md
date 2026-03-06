# Podcast Skill

将文本转换为自然语音播客音频。

## 快速使用

### 在 OpenClaw 中使用

直接对我说：
- "把这段话生成播客：今天天气真好"
- "用男声朗读这篇文章"
- "把今天的调研生成播客并发到我邮箱"

### 命令行使用

```bash
# 基础用法
python3 scripts/generate_podcast.py --text "你的内容"

# 指定语音
python3 scripts/generate_podcast.py --text "你的内容" --voice yunyang

# 从文件读取
python3 scripts/generate_podcast.py --file content.txt

# 发送邮件（首次需配置）
python3 scripts/generate_podcast.py --text "你的内容" --email

# 配置邮箱
python3 scripts/generate_podcast.py --setup
```

## 首次使用邮箱

方式 1：交互式配置
```bash
python3 scripts/generate_podcast.py --setup
```

方式 2：直接提供参数
```bash
python3 scripts/generate_podcast.py \
  --text "内容" \
  --email \
  --recipient user@example.com \
  --sender your@163.com \
  --password 你的授权码
```

## 可用语音

| 代号 | 名称 | 性别 | 风格 |
|------|------|------|------|
| xiaoxiao | 晓晓 | 女 | 温暖亲切（默认） |
| yunyang | 云扬 | 男 | 专业新闻 |
| yunxi | 云希 | 男 | 阳光活泼 |

## 依赖

```bash
pip install edge-tts
```

## 配置文件

用户配置保存在：`~/.podcast-skill/config.json`

可手动编辑此文件修改邮箱配置。

## 支持的邮箱

默认使用 163 邮箱 SMTP，也支持：
- QQ 邮箱：smtp.qq.com, 端口 465
- Gmail：smtp.gmail.com, 端口 587
- Outlook：smtp.office365.com, 端口 587

修改 `config.json` 中的 `smtp_server` 和 `smtp_port` 即可。

---

*Updated: 2026-03-06*
