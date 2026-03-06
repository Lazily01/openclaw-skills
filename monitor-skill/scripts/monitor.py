#!/usr/bin/env python3
"""
Monitor Skill - 网页监控检查
用法：
  python3 monitor.py --url https://example.com --check availability
  python3 monitor.py --url https://item.jd.com/xxx --check price
  python3 monitor.py --url https://example.com --check keyword --keywords "降价,促销"
  python3 monitor.py --url https://example.com --check content
  python3 monitor.py --url https://example.com --check all
"""

import os
import sys
import re
import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error
import ssl
import time

# 配置目录
CONFIG_DIR = Path.home() / ".monitor-skill"
DATA_DIR = CONFIG_DIR / "data"
CONFIG_FILE = CONFIG_DIR / "config.json"

# 默认配置
DEFAULT_CONFIG = {
    "timeout": 30,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
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


def fetch_url(url, config):
    """获取网页内容"""
    timeout = config.get("timeout", 30)
    user_agent = config.get("user_agent", DEFAULT_CONFIG["user_agent"])
    
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(
            url,
            headers={"User-Agent": user_agent}
        )
        
        start = time.time()
        
        with urllib.request.urlopen(req, timeout=timeout, context=context) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            elapsed = (time.time() - start) * 1000  # ms
            status_code = resp.status
            
            return {
                "success": True,
                "content": content,
                "status_code": status_code,
                "elapsed_ms": elapsed
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def check_availability(url, config):
    """检查网站可用性"""
    print(f"🌐 检查可用性: {url}")
    
    result = fetch_url(url, config)
    
    if result["success"]:
        elapsed = result["elapsed_ms"]
        status = result["status_code"]
        
        # 速度评级
        if elapsed < 500:
            speed = "优秀"
        elif elapsed < 1000:
            speed = "良好"
        elif elapsed < 2000:
            speed = "一般"
        else:
            speed = "较慢"
        
        return {
            "status": "ok",
            "available": True,
            "status_code": status,
            "response_time_ms": int(elapsed),
            "speed": speed,
            "message": f"✅ 正常，HTTP {status}，响应时间 {int(elapsed)}ms ({speed})"
        }
    else:
        return {
            "status": "error",
            "available": False,
            "error": result.get("error", "未知错误"),
            "message": f"❌ 不可访问: {result.get('error', '未知错误')}"
        }


def extract_price(content):
    """从网页内容提取价格"""
    patterns = [
        r'¥\s*(\d+\.?\d*)',
        r'￥\s*(\d+\.?\d*)',
        r'价格[：:]\s*(\d+\.?\d*)',
        r'(\d+\.?\d*)\s*元',
        r'price["\']?\s*[:=]\s*["\']?(\d+\.?\d*)',
        r'currentPrice["\']?\s*[:=]\s*["\']?(\d+\.?\d*)',
    ]
    
    prices = []
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            try:
                price = float(match)
                if 0.01 <= price <= 1000000:  # 合理价格范围
                    prices.append(price)
            except:
                pass
    
    if prices:
        # 返回出现最多的价格
        from collections import Counter
        price_counts = Counter(prices)
        most_common = price_counts.most_common(1)[0][0]
        return most_common
    
    return None


def check_price(url, config, threshold=None):
    """检查商品价格"""
    print(f"💰 检查价格: {url}")
    
    result = fetch_url(url, config)
    
    if not result["success"]:
        return {
            "status": "error",
            "error": result.get("error"),
            "message": f"❌ 获取失败: {result.get('error')}"
        }
    
    price = extract_price(result["content"])
    
    if price is not None:
        msg = f"💰 当前价格: ¥{price:.2f}"
        alert = False
        
        if threshold is not None and price <= threshold:
            msg += f" ✅ 已达目标 (目标: ¥{threshold})"
            alert = True
        elif threshold is not None:
            msg += f" (目标: ¥{threshold})"
        
        return {
            "status": "ok",
            "price": price,
            "threshold": threshold,
            "alert": alert,
            "message": msg
        }
    else:
        return {
            "status": "warning",
            "message": "⚠️ 未找到价格信息"
        }


def check_keywords(url, keywords, config):
    """检查关键词"""
    print(f"🔍 检查关键词: {url}")
    
    result = fetch_url(url, config)
    
    if not result["success"]:
        return {
            "status": "error",
            "error": result.get("error"),
            "message": f"❌ 获取失败: {result.get('error')}"
        }
    
    content = result["content"].lower()
    keywords_list = [k.strip().lower() for k in keywords.split(",")]
    
    found = []
    not_found = []
    
    for keyword in keywords_list:
        if keyword in content:
            count = content.count(keyword)
            found.append({"keyword": keyword, "count": count})
        else:
            not_found.append(keyword)
    
    msg_parts = []
    if found:
        found_str = ", ".join([f"'{k['keyword']}'({k['count']}次)" for k in found])
        msg_parts.append(f"发现: {found_str}")
    if not_found:
        msg_parts.append(f"未发现: {', '.join(not_found)}")
    
    return {
        "status": "ok",
        "found": found,
        "not_found": not_found,
        "message": f"🔍 {'; '.join(msg_parts)}"
    }


def check_content_change(url, config):
    """检查内容变化"""
    print(f"📄 检查内容变化: {url}")
    
    result = fetch_url(url, config)
    
    if not result["success"]:
        return {
            "status": "error",
            "error": result.get("error"),
            "message": f"❌ 获取失败: {result.get('error')}"
        }
    
    # 计算内容哈希
    content = result["content"]
    current_hash = hashlib.md5(content.encode()).hexdigest()
    
    # 保存数据目录
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    safe_url = re.sub(r'[^\w]', '_', url)[:50]
    data_file = DATA_DIR / f"{safe_url}.json"
    
    # 读取上次哈希
    last_hash = None
    if data_file.exists():
        with open(data_file, "r") as f:
            data = json.load(f)
            last_hash = data.get("hash")
    
    # 对比
    changed = last_hash is not None and last_hash != current_hash
    
    # 保存当前哈希
    with open(data_file, "w") as f:
        json.dump({
            "hash": current_hash,
            "time": datetime.now().isoformat(),
            "url": url
        }, f)
    
    if changed:
        return {
            "status": "ok",
            "changed": True,
            "hash": current_hash,
            "last_hash": last_hash,
            "message": "🔄 内容已变化！"
        }
    elif last_hash is None:
        return {
            "status": "ok",
            "changed": False,
            "hash": current_hash,
            "message": "📝 首次检查，已记录内容哈希"
        }
    else:
        return {
            "status": "ok",
            "changed": False,
            "hash": current_hash,
            "message": "✅ 内容无变化"
        }


def check_all(url, config, keywords=None, threshold=None):
    """全面检查"""
    print(f"🔍 全面检查: {url}")
    print("-" * 50)
    
    results = {}
    
    # 可用性
    results["availability"] = check_availability(url, config)
    print(f"  {results['availability']['message']}")
    
    if not results["availability"]["available"]:
        return results
    
    # 价格
    results["price"] = check_price(url, config, threshold)
    print(f"  {results['price']['message']}")
    
    # 关键词
    if keywords:
        results["keywords"] = check_keywords(url, keywords, config)
        print(f"  {results['keywords']['message']}")
    
    # 内容变化
    results["content"] = check_content_change(url, config)
    print(f"  {results['content']['message']}")
    
    return results


def generate_report(url, results, output=None):
    """生成检查报告"""
    report = f"""# 网页检查报告

**URL:** {url}
**时间:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

"""
    
    # 可用性
    if "availability" in results:
        avail = results["availability"]
        report += f"""## 🌐 可用性

| 检查项 | 结果 |
|--------|------|
| 状态 | {"✅ 正常" if avail.get("available") else "❌ 异常"} |
| HTTP 状态码 | {avail.get("status_code", "-")} |
| 响应时间 | {avail.get("response_time_ms", "-")}ms |
| 速度评级 | {avail.get("speed", "-")} |

"""
    
    # 价格
    if "price" in results:
        price = results["price"]
        if price.get("price") is not None:
            report += f"""## 💰 价格

| 检查项 | 结果 |
|--------|------|
| 当前价格 | ¥{price.get("price", 0):.2f} |
| 目标价格 | {"¥" + str(price.get("threshold")) if price.get("threshold") else "未设置"} |
| 是否达标 | {"✅ 是" if price.get("alert") else "❌ 否"} |

"""
    
    # 关键词
    if "keywords" in results:
        kw = results["keywords"]
        report += f"""## 🔍 关键词

"""
        if kw.get("found"):
            report += "**发现的关键词:**\n"
            for item in kw["found"]:
                report += f"- {item['keyword']} ({item['count']}次)\n"
        
        if kw.get("not_found"):
            report += "\n**未发现的关键词:**\n"
            for k in kw["not_found"]:
                report += f"- {k}\n"
        
        report += "\n"
    
    # 内容变化
    if "content" in results:
        content = results["content"]
        report += f"""## 📄 内容变化

| 检查项 | 结果 |
|--------|------|
| 是否变化 | {"✅ 是" if content.get("changed") else "❌ 否"} |
| 内容哈希 | `{content.get("hash", "-")}` |

"""
    
    print("\n" + "=" * 50)
    print(report)
    
    # 保存报告
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"📄 报告已保存: {output}")
    
    return report


def main():
    parser = argparse.ArgumentParser(description="Monitor Skill - 网页监控检查")
    
    parser.add_argument("--url", "-u", required=True, help="要检查的 URL")
    parser.add_argument("--check", "-c", 
                       choices=["availability", "price", "keyword", "content", "all"],
                       default="all",
                       help="检查类型")
    parser.add_argument("--keywords", "-k", help="关键词列表（逗号分隔）")
    parser.add_argument("--threshold", "-t", type=float, help="价格阈值")
    parser.add_argument("--output", "-o", help="报告输出路径")
    parser.add_argument("--setup", action="store_true", help="配置")
    
    args = parser.parse_args()
    
    # 配置
    if args.setup:
        print("⚙️ Monitor Skill 配置")
        config = DEFAULT_CONFIG.copy()
        config["timeout"] = int(input("超时时间(秒，默认30): ") or "30")
        save_config(config)
        print(f"✅ 配置已保存: {CONFIG_FILE}")
        return
    
    config = load_config()
    
    print("=" * 50)
    print(f"🔍 Monitor Skill - 网页检查")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 执行检查
    if args.check == "availability":
        result = check_availability(args.url, config)
        results = {"availability": result}
    elif args.check == "price":
        result = check_price(args.url, config, args.threshold)
        results = {"price": result}
    elif args.check == "keyword":
        if not args.keywords:
            print("❌ 请提供关键词: --keywords '关键词1,关键词2'")
            sys.exit(1)
        result = check_keywords(args.url, args.keywords, config)
        results = {"keywords": result}
    elif args.check == "content":
        result = check_content_change(args.url, config)
        results = {"content": result}
    else:  # all
        results = check_all(args.url, config, args.keywords, args.threshold)
    
    # 生成报告
    generate_report(args.url, results, args.output)


if __name__ == "__main__":
    main()
