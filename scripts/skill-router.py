#!/usr/bin/env python3
"""
Skill Semantic Router — matches user input to skill presets.
Integrates algorithms from: MCP-Zero, RAG-MCP, ToolScope, AutoTool.

Usage:
    python3 skill-router.py "渗透测试这个二进制文件"
    → security
    
    python3 skill-router.py "构建一个React组件"  
    → development,design
"""
import sys
import os
import json
import re
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# PRESET DEFINITIONS (from skills-manager pattern)
# ═══════════════════════════════════════════════════════════════

PRESETS = {
    "security": {
        "description": "安全研究/渗透/逆向/漏洞挖掘",
        "keywords": {
            # Chinese
            "渗透": 2, "漏洞": 2, "逆向": 2, "破解": 2, "钓鱼": 2, "恶意": 1.5,
            "二进制": 1.5, "反编译": 1.5, "调试": 1, "注入": 2, "提权": 2,
            "后门": 2, "木马": 2, "病毒": 1.5, "加密": 1, "解密": 1.5,
            "扫描": 1, "爆破": 2, "脱壳": 2, "hook": 1.5, "rootkit": 2,
            # English
            "hack": 2, "exploit": 2, "vulnerability": 2, "pentest": 2,
            "malware": 2, "phishing": 2, "reverse": 1.5, "binary": 1,
            "debug": 1, "inject": 2, "privilege": 2, "backdoor": 2,
            "trojan": 2, "encrypt": 1, "decrypt": 1.5, "scan": 1,
            "brute": 2, "unpack": 2, "rootkit": 2, "drainer": 2,
            "stealer": 2, "keylogger": 2, "ransomware": 2, "ddos": 2,
            "x64dbg": 2, "ida": 2, "ghidra": 2, "ollydbg": 2,
            "cve": 2, "poc": 2, "payload": 2, "shellcode": 2,
            "bounty": 1.5, "赏金": 1.5, "偏门": 1, "黑产": 2, "灰产": 2,
            "绕过": 1.5, "bypass": 1.5, "crack": 2, "keygen": 2,
        },
        "categories": ["red-teaming", "security"],
        "weight": 1.0
    },
    "development": {
        "description": "软件开发/代码/调试/部署",
        "keywords": {
            "代码": 1.5, "开发": 1.5, "构建": 1, "部署": 1.5, "测试": 1,
            "前端": 1.5, "后端": 1.5, "全栈": 1.5, "接口": 1, "数据库": 1,
            "重构": 1.5, "优化": 1, "修复": 1, "bug": 1.5, "功能": 1,
            "模块": 1, "组件": 1, "框架": 1, "库": 1, "包": 1,
            "build": 1.5, "code": 1.5, "debug": 1.5, "test": 1.5,
            "deploy": 1.5, "api": 1.5, "rest": 1, "graphql": 1.5,
            "git": 1.5, "github": 1.5, "pr": 1, "merge": 1, "commit": 1,
            "refactor": 1.5, "fix": 1, "feature": 1.5, "backend": 1.5,
            "frontend": 1.5, "fullstack": 1.5, "react": 1.5, "nextjs": 1.5,
            "python": 1, "typescript": 1.5, "node": 1, "fastapi": 1.5,
            "docker": 1.5, "ci": 1, "cd": 1, "pipeline": 1,
        },
        "categories": ["software-development", "github", "devops"],
        "weight": 1.0
    },
    "design": {
        "description": "UI/UX设计/视觉/品牌",
        "keywords": {
            "设计": 1.5, "界面": 1.5, "样式": 1, "配色": 1.5, "排版": 1.5,
            "logo": 1.5, "品牌": 1.5, "动效": 1.5, "动画": 1, "图标": 1.5,
            "布局": 1.5, "响应式": 1, "主题": 1, "风格": 1.5, "渐变": 1,
            "design": 1.5, "ui": 1.5, "ux": 1.5, "figma": 1.5,
            "css": 1, "tailwind": 1, "component": 1, "layout": 1.5,
            "color": 1.5, "font": 1.5, "typography": 1.5, "spacing": 1,
            "animation": 1.5, "transition": 1, "responsive": 1,
            "毛玻璃": 1, "minimalist": 1.5, "luxury": 1,
        },
        "categories": ["design", "creative"],
        "weight": 1.0
    },
    "daily": {
        "description": "日常工具/效率/办公/通讯",
        "keywords": {
            "提醒": 1.5, "日历": 1.5, "邮件": 1.5, "微信": 1, "文件": 1,
            "办公": 1.5, "文档": 1.5, "pdf": 1.5, "word": 1.5, "excel": 1.5,
            "ppt": 1.5, "笔记": 1, "翻译": 1, "搜索": 1, "天气": 1,
            "remind": 1.5, "calendar": 1.5, "email": 1.5, "wechat": 1,
            "office": 1.5, "document": 1.5, "note": 1, "translate": 1,
            "search": 1, "find": 1, "location": 1, "地图": 1,
        },
        "categories": ["productivity", "automation", "platforms"],
        "weight": 0.8
    },
    "research": {
        "description": "研究/学习/分析/调研",
        "keywords": {
            "研究": 1.5, "论文": 2, "调研": 1.5, "分析": 1, "学习": 1,
            "竞品": 1.5, "市场": 1, "趋势": 1.5, "报告": 1, "数据": 1,
            "research": 1.5, "paper": 2, "arxiv": 2, "analysis": 1,
            "report": 1, "data": 1, "survey": 1.5, "compare": 1,
            "benchmark": 1.5, "evaluate": 1, "统计": 1, "可视化": 1,
        },
        "categories": ["research", "mlops", "autonomous-learning"],
        "weight": 0.9
    },
    "creative": {
        "description": "创意/内容/媒体/社交",
        "keywords": {
            "创作": 1.5, "图片": 1.5, "音乐": 1.5, "视频": 1.5, "漫画": 1.5,
            "小红书": 1.5, "内容": 1, "文章": 1, "故事": 1, "文案": 1.5,
            "海报": 1.5, "封面": 1, "表情包": 1, "头像": 1,
            "art": 1.5, "music": 1.5, "video": 1.5, "photo": 1.5,
            "illustration": 1.5, "image": 1, "generate": 1, "dalle": 1.5,
            "midjourney": 1.5, "stable": 1, "diffusion": 1, "suno": 1.5,
        },
        "categories": ["creative", "media", "social-media"],
        "weight": 0.9
    }
}

# ═══════════════════════════════════════════════════════════════
# ROUTING ALGORITHM (inspired by MCP-Zero two-stage + RAG-MCP)
# ═══════════════════════════════════════════════════════════════

def route(text: str, top_n: int = 2, threshold: float = 0.3) -> str:
    """
    Two-stage routing:
    Stage 1: Keyword matching with weighted scores (RAG-MCP pattern)
    Stage 2: Top-N selection with threshold (MCP-Zero pattern)
    """
    text_lower = text.lower()
    scores = {}
    
    for preset_name, config in PRESETS.items():
        score = 0
        matches = []
        for keyword, weight in config["keywords"].items():
            if keyword.lower() in text_lower:
                score += weight
                matches.append(keyword)
        
        # Normalize by keyword count to avoid bias toward presets with more keywords
        normalized = score / max(len(config["keywords"]) * 0.1, 1)
        scores[preset_name] = {
            "raw": score,
            "normalized": normalized,
            "matches": matches
        }
    
    # Sort by normalized score
    sorted_presets = sorted(
        scores.items(), 
        key=lambda x: x[1]["normalized"], 
        reverse=True
    )
    
    # Filter by threshold
    results = []
    for name, data in sorted_presets:
        if data["normalized"] >= threshold:
            results.append(name)
        if len(results) >= top_n:
            break
    
    # Fallback
    if not results:
        results = ["daily"]
    
    return ",".join(results)


def get_preset_skills(preset_name: str) -> list:
    """Get the skill names for a given preset."""
    # This would read from skill-presets.yaml in production
    return PRESETS.get(preset_name, {}).get("skills", [])


def route_with_details(text: str) -> dict:
    """Route with full details for debugging."""
    text_lower = text.lower()
    results = {}
    
    for preset_name, config in PRESETS.items():
        score = 0
        matches = []
        for keyword, weight in config["keywords"].items():
            if keyword.lower() in text_lower:
                score += weight
                matches.append({"keyword": keyword, "weight": weight})
        
        normalized = score / max(len(config["keywords"]) * 0.1, 1)
        results[preset_name] = {
            "description": config["description"],
            "raw_score": round(score, 2),
            "normalized_score": round(normalized, 4),
            "matches": matches,
            "match_count": len(matches)
        }
    
    sorted_results = sorted(
        results.items(),
        key=lambda x: x[1]["normalized_score"],
        reverse=True
    )
    
    return {
        "input": text,
        "rankings": sorted_results,
        "recommended": [name for name, data in sorted_results if data["normalized_score"] >= 0.3][:2]
    }


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 skill-router.py <text>")
        print("       python3 skill-router.py --details <text>")
        sys.exit(1)
    
    if sys.argv[1] == "--details":
        text = " ".join(sys.argv[2:])
        result = route_with_details(text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        text = " ".join(sys.argv[1:])
        print(route(text))
