---
name: doubao-image-generation
description: "使用火山引擎豆包 Seedream 4.5 生成高质量 AI 图片。支持 2K-4K 分辨率、去水印、多风格。主动使用场景：用户需要配图、插图、概念图、产品图、艺术创作时自动调用。"
allowed-tools: Bash(curl *)
---

# 豆包生图技能

## 配置信息

- **API Key:** `2073fda9-6860-4979-93a5-6ca8d7ec4c5b`
- **端点:** `https://ark.cn-beijing.volces.com/api/v3/images/generations`
- **模型:** Seedream 4.5 (`ep-20251205202908-h9vmw`)

## 快速调用

```bash
curl -X POST 'https://ark.cn-beijing.volces.com/api/v3/images/generations' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer 2073fda9-6860-4979-93a5-6ca8d7ec4c5b' \
  -d '{
    "model": "ep-20251205202908-h9vmw",
    "prompt": "图片描述",
    "size": "4096x2160",
    "watermark": false
  }'
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `prompt` | 图片描述（中文/英文均可） |
| `size` | 分辨率：`2048x2048`、`4096x2160`（4K）、`2160x4096` |
| `watermark` | `false` 无水印，`true` 右下角"AI生成" |

## 尺寸限制

- 最小：3,686,400 像素（2048x2048）
- 最大：16,777,216 像素
- 宽高比：[1/16, 16]

## 使用场景

**主动调用触发词：**
- 配图、插图、封面图
- 概念图、效果图
- 产品图、宣传图
- AI 艺术创作
- "生成图片"、"画一张"、"做个图"

**返回值：**
- 图片链接（24小时有效）
- 自动下载到桌面或指定位置

## 示例

### 4K 无水印图片

```bash
curl -X POST 'https://ark.cn-beijing.volces.com/api/v3/images/generations' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer 2073fda9-6860-4979-93a5-6ca8d7ec4c5b' \
  -d '{
    "model": "ep-20251205202908-h9vmw",
    "prompt": "赛博朋克风格的城市夜景，霓虹灯，雨后反射，电影质感",
    "size": "4096x2160",
    "watermark": false
  }'
```

### 正方形配图

```bash
curl -X POST 'https://ark.cn-beijing.volces.com/api/v3/images/generations' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer 2073fda9-6860-4979-93a5-6ca8d7ec4c5b' \
  -d '{
    "model": "ep-20251205202908-h9vmw",
    "prompt": "简洁的产品展示图，白色背景，柔和光照",
    "size": "2048x2048",
    "watermark": false
  }'
```

## 注意事项

1. 图片链接 24 小时内有效
2. 高峰期可能稍慢
3. 复杂描述效果更好
4. 支持中英文 prompt
