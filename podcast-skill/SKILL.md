# Podcast Skill - 文本转播客音频

## 触发场景

当用户说以下内容时，自动触发此 skill：
- "生成播客"
- "把这段文字转成音频"
- "朗读这篇文章"
- "用 TTS 生成"
- "语音合成"
- "念给我听"

## 功能

将文本内容转换为自然语音播客音频，支持：
- 多种中文语音（男声/女声）
- 自定义邮箱配置
- 邮件发送
- 保存到本地

## 使用示例

### 基础用法
```
用户：把这段话生成播客："今天天气真好，适合出门散步。"
→ 生成音频，使用默认女声（晓晓）
```

### 指定语音
```
用户：用男声朗读这段话
→ 使用男声（云扬）
```

### 从文件生成
```
用户：把今天的调研生成播客
→ 读取文件 → 生成音频
```

### 发送到邮箱（首次需配置）
```
用户：生成播客并发到我邮箱
→ 生成音频 → 发送邮件
```

## 首次使用邮箱

用户需要先配置邮箱信息：
```bash
python3 scripts/generate_podcast.py --setup
```

或直接提供参数：
```bash
python3 scripts/generate_podcast.py --text "内容" --email --recipient user@example.com --sender your@163.com --password 授权码
```

## 可用语音

| 语音代号 | 名称 | 性别 | 特点 |
|----------|------|------|------|
| xiaoxiao | 晓晓 | 女 | 温暖亲切（默认） |
| yunyang | 云扬 | 男 | 专业新闻风 |
| yunxi | 云希 | 男 | 阳光活泼 |

## 技术实现

使用 edge-tts（微软 Edge TTS，免费）：

```bash
# 基础命令
edge-tts --voice zh-CN-XiaoxiaoNeural --text "内容" --write-media output.mp3
```

## 配置存储

用户配置保存在：`~/.podcast-skill/config.json`

```json
{
  "email_sender": "your@163.com",
  "email_password": "授权码",
  "email_recipient": "recipient@example.com",
  "smtp_server": "smtp.163.com",
  "smtp_port": 465,
  "default_voice": "xiaoxiao"
}
```

## 工作流程

1. **接收请求** — 用户说"生成播客"
2. **解析参数** — 语音类型、是否发邮件
3. **准备内容** — 直接文本 或 读取文件
4. **生成音频** — 调用 TTS
5. **发送邮件** — 如需发邮件，检查配置
6. **输出结果** — 返回音频路径

---

*Updated: 2026-03-06*
