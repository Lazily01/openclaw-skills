#!/usr/bin/env python3
"""
Podcast Skill - 生成播客音频
用法：python3 generate_podcast.py --text "内容" --voice xiaoxiao --email --recipient user@example.com
"""

import os
import sys
import subprocess
import argparse
import json
from datetime import datetime
from pathlib import Path

# 配置目录
CONFIG_DIR = Path.home() / ".podcast-skill"
CONFIG_FILE = CONFIG_DIR / "config.json"

# 默认配置模板
DEFAULT_CONFIG = {
    "email_sender": "",
    "email_password": "",
    "email_recipient": "",
    "smtp_server": "smtp.163.com",
    "smtp_port": 465,
    "default_voice": "xiaoxiao"
}

# 输出目录
OUTPUT_DIR = Path.home() / ".podcast-skill" / "output"

# 语音映射
VOICES = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",   # 女 - 温暖亲切（默认）
    "yunyang": "zh-CN-YunyangNeural",     # 男 - 专业新闻
    "yunxi": "zh-CN-YunxiNeural",         # 男 - 阳光活泼
}


def load_config():
    """加载配置"""
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    """保存配置"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def setup_email_config():
    """引导用户配置邮箱"""
    print("📧 首次使用，请配置邮箱信息")
    print("-" * 40)
    
    config = DEFAULT_CONFIG.copy()
    
    config["email_sender"] = input("发件邮箱 (例: your@163.com): ").strip()
    config["email_password"] = input("授权码 (不是邮箱密码): ").strip()
    config["email_recipient"] = input("收件邮箱: ").strip()
    
    save_config(config)
    print(f"\n✅ 配置已保存到: {CONFIG_FILE}")
    return config


def generate_audio(text, voice="xiaoxiao", output_path=None):
    """生成播客音频"""
    voice_id = VOICES.get(voice, VOICES["xiaoxiao"])
    
    if not output_path:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_path = OUTPUT_DIR / f"podcast_{today}.mp3"
    
    print(f"🎙️ 生成播客音频...")
    print(f"   语音: {voice} ({voice_id})")
    print(f"   内容长度: {len(text)} 字")
    
    # 调用 edge-tts
    cmd = [
        "edge-tts",
        "--voice", voice_id,
        "--text", text,
        "--write-media", str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ 音频已生成: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"❌ 生成失败: {e.stderr.decode() if e.stderr else str(e)}")
        return None


def send_email(audio_path, recipient=None, sender=None, password=None, smtp_server=None, smtp_port=None, subject="AI 播客"):
    """发送邮件"""
    # 优先使用参数，其次使用配置
    config = load_config()
    
    sender = sender or config.get("email_sender")
    password = password or config.get("email_password")
    recipient = recipient or config.get("email_recipient")
    smtp_server = smtp_server or config.get("smtp_server", "smtp.163.com")
    smtp_port = smtp_port or config.get("smtp_port", 465)
    
    if not all([sender, password, recipient]):
        print("❌ 缺少邮箱配置，请运行 --setup 或提供参数")
        return False
    
    print(f"📧 发送邮件到 {recipient}...")
    
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email import encoders
        
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = subject
        
        # 正文
        body = f"""
你好！

这是生成的播客音频，请查收。

文件: {audio_path.name}
时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

祝好！
AI 播客助手
"""
        msg.attach(MIMEText(body, "plain", "utf-8"))
        
        # 附件
        with open(audio_path, "rb") as f:
            part = MIMEBase("audio", "mpeg")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment", filename=audio_path.name)
            msg.attach(part)
        
        # 发送
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        
        print(f"✅ 邮件已发送")
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="生成播客音频")
    parser.add_argument("--text", "-t", help="播客文本内容")
    parser.add_argument("--file", "-f", help="从文件读取内容")
    parser.add_argument("--voice", "-v", default="xiaoxiao", 
                       choices=["xiaoxiao", "yunyang", "yunxi"],
                       help="语音类型（默认: xiaoxiao）")
    parser.add_argument("--email", "-e", action="store_true", help="发送到邮箱")
    parser.add_argument("--recipient", "-r", help="收件邮箱（覆盖配置）")
    parser.add_argument("--sender", "-s", help="发件邮箱（覆盖配置）")
    parser.add_argument("--password", "-p", help="邮箱授权码（覆盖配置）")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--setup", action="store_true", help="配置邮箱信息")
    
    args = parser.parse_args()
    
    # 配置邮箱
    if args.setup:
        setup_email_config()
        return
    
    # 获取文本
    text = args.text
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    
    if not text:
        print("❌ 请提供文本内容 (--text 或 --file)")
        sys.exit(1)
    
    # 生成音频
    audio_path = generate_audio(text, args.voice, args.output)
    if not audio_path:
        sys.exit(1)
    
    # 发送邮件
    if args.email:
        send_email(
            audio_path,
            recipient=args.recipient,
            sender=args.sender,
            password=args.password
        )
    
    print(f"\n🎉 完成！音频文件: {audio_path}")


if __name__ == "__main__":
    main()
