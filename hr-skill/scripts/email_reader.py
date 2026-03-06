#!/usr/bin/env python3
"""
HR Skill - 邮件简历获取模块
从邮箱批量获取简历附件
"""

import os
import sys
import imaplib
import email
from email.header import decode_header
from pathlib import Path
from datetime import datetime

# 简历关键词
RESUME_KEYWORDS = ["简历", "应聘", "求职", "resume", "cv", "申请"]

# 跳过关键词
SKIP_KEYWORDS = ["验证码", "播客", "podcast", "通知", "提醒", "广告"]


def decode_str(s):
    """解码邮件头字符串"""
    if s is None:
        return ""
    
    decoded_parts = decode_header(s)
    result = []
    
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            charset = charset or "utf-8"
            try:
                result.append(part.decode(charset, errors="ignore"))
            except:
                result.append(part.decode("utf-8", errors="ignore"))
        else:
            result.append(part)
    
    return "".join(result)


def is_resume_email(subject, from_addr):
    """判断是否是简历邮件"""
    subject_lower = subject.lower()
    
    # 检查跳过关键词
    for keyword in SKIP_KEYWORDS:
        if keyword.lower() in subject_lower:
            return False, f"跳过: 包含非简历关键词 '{keyword}'"
    
    # 检查简历关键词
    for keyword in RESUME_KEYWORDS:
        if keyword.lower() in subject_lower:
            return True, f"识别为简历: 包含关键词 '{keyword}'"
    
    # 检查发件人是否是招聘平台
    recruitment_platforms = [
        "boss", "zhipin", "liepin", "51job", "zhaopin",
        "linkedin", "indeed", "recruit"
    ]
    for platform in recruitment_platforms:
        if platform in from_addr.lower():
            return True, "识别为简历: 来自招聘平台"
    
    return False, "跳过: 不符合简历特征"


def extract_attachments(msg, output_dir):
    """提取邮件附件"""
    attachments = []
    
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        if not part.get("Content-Disposition"):
            continue
        
        filename = part.get_filename()
        if filename:
            filename = decode_str(filename)
            ext = os.path.splitext(filename)[1].lower()
            
            # 只处理 PDF 和 Word 文件
            if ext in [".pdf", ".doc", ".docx"]:
                filepath = os.path.join(output_dir, filename)
                
                # 文件已存在则跳过
                if os.path.exists(filepath):
                    print(f"  ⏭️ 已存在，跳过: {filename}")
                    attachments.append(filepath)
                    continue
                
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                
                attachments.append(filepath)
                print(f"  📎 保存附件: {filename}")
    
    return attachments


def read_emails_from_imap(
    imap_server,
    imap_port,
    email_addr,
    password,
    output_dir,
    limit=50
):
    """从 IMAP 邮箱读取简历邮件"""
    import ssl
    
    print(f"📬 连接邮箱: {email_addr}")
    
    try:
        # 连接 IMAP
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(imap_server, imap_port, ssl_context=context)
        
        # 登录
        mail.login(email_addr, password)
        print(f"✅ 登录成功\n")
        
        # 选择收件箱
        mail.select("INBOX")
        
        # 搜索邮件
        status, messages = mail.search(None, "ALL")
        email_ids = messages[0].split()
        
        total = len(email_ids)
        print(f"📬 收件箱共 {total} 封邮件")
        print(f"🔍 检查最近 {min(limit, total)} 封邮件...\n")
        
        # 获取最近的邮件
        recent_ids = email_ids[-limit:] if limit else email_ids
        recent_ids.reverse()  # 最新的先处理
        
        resumes = []
        checked = 0
        
        for email_id in recent_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # 解析邮件
                    subject = decode_str(msg.get("Subject", ""))
                    from_addr = decode_str(msg.get("From", ""))
                    date = msg.get("Date", "")
                    
                    # 判断是否是简历邮件
                    is_resume, reason = is_resume_email(subject, from_addr)
                    
                    if is_resume:
                        checked += 1
                        print(f"-" * 50)
                        print(f"📧 简历邮件 #{checked}")
                        print(f"   主题: {subject}")
                        print(f"   发件人: {from_addr}")
                        print(f"   日期: {date}")
                        print(f"   识别: {reason}")
                        
                        # 提取附件
                        attachments = extract_attachments(msg, output_dir)
                        
                        if attachments:
                            resumes.append({
                                "subject": subject,
                                "from": from_addr,
                                "date": date,
                                "attachments": attachments
                            })
        
        mail.logout()
        
        print(f"\n{'=' * 50}")
        print(f"✅ 检查完成")
        print(f"   检查邮件: {checked} 封")
        print(f"   发现简历: {len(resumes)} 封")
        print(f"   保存目录: {output_dir}")
        
        return resumes
        
    except Exception as e:
        print(f"❌ 邮箱读取失败: {e}")
        return []


def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="从邮箱获取简历")
    parser.add_argument("--config", "-c", help="配置文件路径")
    parser.add_argument("--output", "-o", default="resumes", help="输出目录")
    parser.add_argument("--limit", "-l", type=int, default=50, help="检查邮件数量")
    parser.add_argument("--server", "-s", help="IMAP 服务器")
    parser.add_argument("--port", "-p", type=int, default=993, help="IMAP 端口")
    parser.add_argument("--email", "-e", help="邮箱地址")
    parser.add_argument("--password", "-P", help="邮箱密码/授权码")
    
    args = parser.parse_args()
    
    # 加载配置
    config = {}
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
    
    # 参数优先
    imap_server = args.server or config.get("imap_server")
    imap_port = args.port or config.get("imap_port", 993)
    email_addr = args.email or config.get("imap_email") or config.get("email_sender")
    password = args.password or config.get("imap_password") or config.get("email_password")
    
    if not all([imap_server, email_addr, password]):
        print("❌ 缺少邮箱配置")
        print("   请提供 --server, --email, --password 或使用 --config 指定配置文件")
        sys.exit(1)
    
    # 输出目录
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取邮件
    resumes = read_emails_from_imap(
        imap_server,
        imap_port,
        email_addr,
        password,
        output_dir,
        args.limit
    )
    
    # 输出结果
    if resumes:
        print(f"\n📎 简历附件保存在: {output_dir}")


if __name__ == "__main__":
    main()
