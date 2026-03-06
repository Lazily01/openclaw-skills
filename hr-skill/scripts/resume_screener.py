#!/usr/bin/env python3
"""
HR Skill - 简历智能筛选
用法：
  python3 resume_screener.py --file resume.pdf --job 运营总监
  python3 resume_screener.py --dir resumes/ --job 运营总监
  python3 resume_screener.py --add-job 运营总监
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# 配置目录
SKILL_DIR = Path(__file__).parent.parent
JOBS_DIR = SKILL_DIR / "jobs"
CONFIG_DIR = Path.home() / ".hr-skill"
CONFIG_FILE = CONFIG_DIR / "config.json"
OUTPUT_DIR = CONFIG_DIR / "reports"

# 默认配置
DEFAULT_CONFIG = {
    "api_provider": "zai",  # zai / openai / anthropic
    "api_key": "",
    "model": "glm-5",
    # 邮件发送（报告）
    "email_sender": "",
    "email_password": "",
    "email_recipient": "",
    "smtp_server": "smtp.163.com",
    "smtp_port": 465,
    # 邮件接收（简历）
    "imap_server": "",
    "imap_port": 993,
    "imap_email": "",
    "imap_password": ""
}

# 简历解析 Prompt
RESUME_PROMPT = """请提取这份简历的关键信息，输出 JSON 格式：
{
  "name": "姓名",
  "phone": "手机号",
  "email": "邮箱",
  "experience_years": 工作年限(数字),
  "current_position": "当前职位",
  "skills": ["技能1", "技能2"],
  "education": "学历",
  "education_detail": "学校/专业",
  "work_history": [{"company": "公司", "position": "职位", "years": 年限}],
  "summary": "一句话简介"
}

简历内容：
{text}
"""

# 匹配评估 Prompt
MATCH_PROMPT = """请评估这位候选人与岗位的匹配度，输出 JSON 格式：
{
  "match_score": 匹配度(0-100的数字),
  "star_rating": 星级(1-5),
  "matched_skills": ["匹配的技能"],
  "missing_skills": ["缺失的技能"],
  "strengths": ["优势"],
  "concerns": ["顾虑"],
  "recommendation": "推荐/可考虑/不推荐",
  "reason": "推荐理由"
}

岗位要求：
{job_requirements}

候选人信息：
{candidate_info}
"""


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


def setup_config():
    """交互式配置"""
    print("⚙️ HR Skill 配置")
    print("-" * 40)
    
    config = DEFAULT_CONFIG.copy()
    
    print("\n📡 LLM API 配置（用于独立运行，可选）")
    config["api_provider"] = input("API 提供商 (zai/openai/anthropic，回车跳过): ").strip() or "zai"
    config["api_key"] = input("API Key（回车跳过）: ").strip()
    config["model"] = input("模型名称 (默认 glm-5): ").strip() or "glm-5"
    
    print("\n📧 邮箱发送配置（用于发送报告，可选）")
    config["email_sender"] = input("发件邮箱（回车跳过）: ").strip()
    if config["email_sender"]:
        config["email_password"] = input("授权码: ").strip()
        config["email_recipient"] = input("收件邮箱: ").strip()
    
    print("\n📬 邮箱接收配置（用于获取简历，可选）")
    config["imap_email"] = input("IMAP 邮箱（回车跳过）: ").strip()
    if config["imap_email"]:
        config["imap_server"] = input("IMAP 服务器 (默认 imap.qq.com): ").strip() or "imap.qq.com"
        config["imap_port"] = int(input("IMAP 端口 (默认 993): ").strip() or "993")
        config["imap_password"] = input("邮箱授权码: ").strip()
    
    save_config(config)
    print(f"\n✅ 配置已保存到: {CONFIG_FILE}")


def load_jobs():
    """加载所有岗位配置"""
    jobs = {}
    if not JOBS_DIR.exists():
        return jobs
    
    for job_file in JOBS_DIR.glob("*.json"):
        with open(job_file, "r", encoding="utf-8") as f:
            job = json.load(f)
            jobs[job["title"]] = job
    
    return jobs


def add_job_interactive():
    """交互式添加岗位"""
    print("📋 添加岗位配置")
    print("-" * 40)
    
    job = {}
    job["title"] = input("岗位名称: ").strip()
    job["required_experience"] = int(input("要求工作年限 (数字): ").strip() or "0")
    job["required_education"] = input("要求学历 (本科/硕士/博士/不限): ").strip() or "不限"
    
    skills_input = input("必备技能 (逗号分隔): ").strip()
    job["required_skills"] = [s.strip() for s in skills_input.split(",")] if skills_input else []
    
    bonus_input = input("加分技能 (逗号分隔): ").strip()
    job["bonus_skills"] = [s.strip() for s in bonus_input.split(",")] if bonus_input else []
    
    job["description"] = input("岗位描述 (可选): ").strip()
    
    # 保存
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    job_file = JOBS_DIR / f"{job['title']}.json"
    with open(job_file, "w", encoding="utf-8") as f:
        json.dump(job, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 岗位已保存: {job_file}")
    return job


def extract_text_from_pdf(filepath):
    """从 PDF 提取文本"""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except ImportError:
        print("⚠️ 需要安装 PyMuPDF: pip install pymupdf")
        return ""


def extract_text_from_docx(filepath):
    """从 Word 提取文本"""
    try:
        from docx import Document
        doc = Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    except ImportError:
        print("⚠️ 需要安装 python-docx: pip install python-docx")
        return ""


def extract_text(filepath):
    """根据文件类型提取文本"""
    ext = Path(filepath).suffix.lower()
    
    if ext == ".pdf":
        return extract_text_from_pdf(filepath)
    elif ext in [".doc", ".docx"]:
        return extract_text_from_docx(filepath)
    elif ext == ".txt":
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    else:
        print(f"⚠️ 不支持的文件格式: {ext}")
        return ""


def parse_resume_with_llm(text, config):
    """使用 LLM 解析简历"""
    import requests
    
    api_provider = config.get("api_provider", "zai")
    api_key = config.get("api_key", "")
    model = config.get("model", "glm-5")
    
    if not api_key:
        print("❌ 未配置 API Key，无法使用 LLM 解析")
        print("   请运行 --setup 配置，或通过 OpenClaw 调用")
        return None
    
    # 根据提供商调用 API
    if api_provider == "zai":
        url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    elif api_provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    else:
        print(f"❌ 不支持的 API 提供商: {api_provider}")
        return None
    
    prompt = RESUME_PROMPT.format(text=text[:3000])  # 限制长度
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        
        # 提取 JSON
        content = result["choices"][0]["message"]["content"]
        
        # 尝试解析 JSON
        import re
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            return json.loads(json_match.group())
        
        return {"raw": content, "parse_error": True}
        
    except Exception as e:
        print(f"❌ LLM 调用失败: {e}")
        return None


def match_candidate(resume_info, job, config):
    """评估候选人匹配度"""
    import requests
    
    api_key = config.get("api_key", "")
    if not api_key:
        # 简单匹配逻辑（无 LLM）
        return simple_match(resume_info, job)
    
    # 使用 LLM 评估
    # ... 类似 parse_resume_with_llm 的逻辑
    pass


def simple_match(resume_info, job):
    """简单匹配逻辑（不需要 API）"""
    score = 0
    
    # 经验匹配 (30分)
    exp_years = resume_info.get("experience_years", 0)
    required_exp = job.get("required_experience", 0)
    if exp_years >= required_exp:
        score += 30
    elif exp_years >= required_exp * 0.7:
        score += 20
    
    # 技能匹配 (50分)
    skills = [s.lower() for s in resume_info.get("skills", [])]
    required_skills = [s.lower() for s in job.get("required_skills", [])]
    bonus_skills = [s.lower() for s in job.get("bonus_skills", [])]
    
    matched = sum(1 for s in required_skills if any(s in skill for skill in skills))
    if required_skills:
        score += (matched / len(required_skills)) * 40
    
    # 加分项 (20分)
    bonus_matched = sum(1 for s in bonus_skills if any(s in skill for skill in skills))
    if bonus_skills:
        score += min((bonus_matched / len(bonus_skills)) * 20, 20)
    
    # 星级
    if score >= 90:
        star = 5
    elif score >= 75:
        star = 4
    elif score >= 60:
        star = 3
    elif score >= 40:
        star = 2
    else:
        star = 1
    
    return {
        "match_score": int(score),
        "star_rating": star,
        "matched_skills": [s for s in required_skills if any(s in skill for skill in skills)],
        "recommendation": "推荐" if star >= 4 else "可考虑" if star >= 3 else "不推荐"
    }


def generate_report(results, job_title):
    """生成筛选报告"""
    # 按匹配度排序
    results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
    
    report = f"""# 简历筛选报告

**岗位：** {job_title}
**日期：** {datetime.now().strftime("%Y-%m-%d")}
**处理数量：** {len(results)} 份

---

"""
    
    # 按星级分组
    groups = {5: [], 4: [], 3: [], 2: [], 1: []}
    for r in results:
        star = r.get("star_rating", 1)
        groups[star].append(r)
    
    star_labels = {
        5: "⭐⭐⭐⭐⭐ 强烈推荐",
        4: "⭐⭐⭐⭐ 推荐",
        3: "⭐⭐⭐ 可考虑",
        2: "⭐⭐ 不太匹配",
        1: "⭐ 不推荐"
    }
    
    for star in [5, 4, 3, 2, 1]:
        if not groups[star]:
            continue
        
        report += f"## {star_labels[star]}\n\n"
        
        for i, r in enumerate(groups[star], 1):
            resume = r.get("resume", {})
            report += f"""### {i}. {resume.get('name', '未知')} - {resume.get('experience_years', 0)}年经验

- **匹配度：** {r.get('match_score', 0)}%
- **当前职位：** {resume.get('current_position', '未知')}
- **学历：** {resume.get('education', '未知')}
- **技能：** {', '.join(resume.get('skills', [])[:5]) or '未识别'}
- **联系方式：** {resume.get('phone', '')} | {resume.get('email', '')}
- **推荐理由：** {r.get('recommendation', '')}

"""
    
    return report


def save_report(report, filename=None):
    """保存报告"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if not filename:
        filename = f"report_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.md"
    
    filepath = OUTPUT_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"📄 报告已保存: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="HR Skill - 简历智能筛选")
    
    # 操作
    parser.add_argument("--setup", action="store_true", help="配置 API 和邮箱")
    parser.add_argument("--add-job", action="store_true", help="添加岗位配置")
    parser.add_argument("--list-jobs", action="store_true", help="列出所有岗位")
    
    # 筛选
    parser.add_argument("--file", "-f", help="单个简历文件")
    parser.add_argument("--dir", "-d", help="简历文件夹")
    parser.add_argument("--from-email", action="store_true", help="从邮箱获取简历")
    parser.add_argument("--email-limit", type=int, default=50, help="邮箱检查数量")
    parser.add_argument("--job", "-j", help="匹配的岗位名称")
    parser.add_argument("--text", "-t", help="直接提供简历文本")
    
    # 输出
    parser.add_argument("--output", "-o", help="报告输出路径")
    parser.add_argument("--send-email", action="store_true", help="发送报告到邮箱")
    
    args = parser.parse_args()
    
    # 配置
    if args.setup:
        setup_config()
        return
    
    # 添加岗位
    if args.add_job:
        add_job_interactive()
        return
    
    # 列出岗位
    if args.list_jobs:
        jobs = load_jobs()
        if not jobs:
            print("暂无岗位配置，请使用 --add-job 添加")
        else:
            print("📋 已配置岗位：")
            for title, job in jobs.items():
                print(f"  - {title} ({job.get('required_experience', 0)}年+)")
        return
    
    # 筛选简历
    if not args.file and not args.dir and not args.text and not args.from_email:
        print("❌ 请提供简历文件 (--file) 或文件夹 (--dir) 或从邮箱获取 (--from-email)")
        print("   或使用 --setup 配置，--add-job 添加岗位")
        sys.exit(1)
    
    # 加载岗位
    jobs = load_jobs()
    if not jobs:
        print("❌ 暂无岗位配置，请先添加岗位: --add-job")
        sys.exit(1)
    
    if args.job and args.job not in jobs:
        print(f"❌ 未找到岗位: {args.job}")
        print(f"   可用岗位: {', '.join(jobs.keys())}")
        sys.exit(1)
    
    job = jobs.get(args.job, list(jobs.values())[0])
    config = load_config()
    
    # 收集简历
    resume_files = []
    
    # 从邮箱获取
    if args.from_email:
        from email_reader import read_emails_from_imap
        
        imap_server = config.get("imap_server")
        imap_port = config.get("imap_port", 993)
        imap_email = config.get("imap_email")
        imap_password = config.get("imap_password")
        
        if not all([imap_server, imap_email, imap_password]):
            print("❌ 未配置 IMAP 邮箱，请先运行 --setup")
            sys.exit(1)
        
        # 创建临时目录
        temp_dir = CONFIG_DIR / "resumes"
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        print("📬 从邮箱获取简历...")
        read_emails_from_imap(
            imap_server,
            imap_port,
            imap_email,
            imap_password,
            str(temp_dir),
            args.email_limit
        )
        
        # 收集文件
        resume_files = list(temp_dir.glob("*.pdf")) + \
                       list(temp_dir.glob("*.doc")) + \
                       list(temp_dir.glob("*.docx"))
    
    # 从本地文件
    if args.file:
        resume_files = [Path(args.file)]
    elif args.dir:
        resume_dir = Path(args.dir)
        resume_files = list(resume_dir.glob("*.pdf")) + \
                       list(resume_dir.glob("*.doc")) + \
                       list(resume_dir.glob("*.docx"))
    
    if not resume_files and not args.text:
        print("❌ 未找到简历文件")
        sys.exit(1)
    
    print(f"📋 岗位: {job['title']}")
    print(f"📄 简历数量: {len(resume_files)}")
    print("-" * 40)
    
    # 解析简历
    results = []
    for resume_file in resume_files:
        print(f"\n📄 解析: {resume_file.name}")
        
        text = extract_text(resume_file)
        if not text:
            continue
        
        # 尝试 LLM 解析
        resume_info = parse_resume_with_llm(text, config)
        
        if not resume_info:
            # 简单提取
            resume_info = {"file": str(resume_file), "raw_text": text[:500]}
        
        resume_info["file"] = str(resume_file)
        
        # 匹配评估
        match_result = simple_match(resume_info, job)
        match_result["resume"] = resume_info
        
        results.append(match_result)
        print(f"   匹配度: {match_result['match_score']}% {'⭐' * match_result['star_rating']}")
    
    # 生成报告
    if results:
        report = generate_report(results, job["title"])
        print("\n" + "=" * 40)
        print(report[:500] + "...")
        
        filepath = save_report(report, args.output)
        
        if args.send_email:
            print("📧 发送邮件功能待实现")


if __name__ == "__main__":
    main()
