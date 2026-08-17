#!/usr/bin/env python3
"""
Quick Start Template for Automated Revenue Scheme
快速启动模板 - 自动化收益方案
"""

import os
import sys
from pathlib import Path

def create_project_structure(project_name):
    """创建项目目录结构"""
    base_dir = Path(project_name)
    
    directories = [
        base_dir / "data",
        base_dir / "reports",
        base_dir / "automation" / "scripts",
        base_dir / "automation" / "config",
        base_dir / "templates",
        base_dir / "web" / "static",
        base_dir / "web" / "templates",
        base_dir / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return base_dir

def create_config_file(project_dir):
    """创建配置文件"""
    config_content = """# Project Configuration
project_name: "Auto-Tech-Trend"
version: "1.0.0"
description: "Automated technology trend analysis service"

# Data Sources
data_sources:
  - name: "GitHub"
    api_url: "https://api.github.com"
    min_stars: 500
    limit: 10
    update_frequency: "weekly"

# Email Settings
email:
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  sender_email: "reports@example.com"
  sender_name: "Auto-Tech-Trend Reports"
  
# Pricing Tiers
pricing:
  free:
    price: 0
    features: ["weekly_summary", "basic_reports"]
  pro:
    price: 29
    features: ["full_reports", "api_access", "email_support"]
  enterprise:
    price: 99
    features: ["custom_analysis", "consulting", "white_label"]

# Automation Settings
automation:
  schedule: "weekly"
  day: "monday"
  time: "09:00"
  timezone: "UTC"
"""
    
    config_path = project_dir / "config" / "settings.yaml"
    with open(config_path, "w") as f:
        f.write(config_content)
    
    print(f"✅ Created config file: {config_path}")
    return config_path

def create_data_collection_script(project_dir):
    """创建数据收集脚本"""
    script_content = '''#!/usr/bin/env python3
"""
Data Collection Script
数据收集脚本
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

def collect_trending_data(min_stars=500, limit=10):
    """收集GitHub趋势数据"""
    print("📡 Collecting GitHub trending data...")
    
    cmd = f'curl -s "https://api.github.com/search/repositories?q=stars:>{min_stars}&sort=updated&order=desc"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Failed to fetch data")
        return None
    
    try:
        data = json.loads(result.stdout)
        repos = data.get("items", [])[:limit]
        print(f"✅ Collected {len(repos)} repositories")
        return repos
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        return None

def save_data(repos, output_path):
    """保存数据到文件"""
    timestamp = datetime.now().isoformat()
    
    data = {
        "collected_at": timestamp,
        "repositories": repos,
        "count": len(repos)
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Data saved to: {output_path}")

def main():
    """主函数"""
    # 配置
    min_stars = 500
    limit = 10
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)
    
    # 收集数据
    repos = collect_trending_data(min_stars, limit)
    
    if repos:
        # 保存数据
        output_file = output_dir / f"trending_{datetime.now().strftime('%Y%m%d')}.json"
        save_data(repos, output_file)
        print(f"✅ Data collection complete: {output_file}")
    else:
        print("❌ Data collection failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    script_path = project_dir / "automation" / "scripts" / "collect_data.py"
    with open(script_path, "w") as f:
        f.write(script_content)
    
    print(f"✅ Created data collection script: {script_path}")
    return script_path

def main():
    """主函数"""
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
    else:
        project_name = "automated-revenue-project"
    
    print(f"🚀 Creating automated revenue project: {project_name}")
    print("=" * 50)
    
    # 创建项目结构
    project_dir = create_project_structure(project_name)
    
    # 创建配置文件
    create_config_file(project_dir)
    
    # 创建数据收集脚本
    create_data_collection_script(project_dir)
    
    print("=" * 50)
    print("✅ Project created successfully!")
    print(f"📁 Location: {project_dir.absolute()}")

if __name__ == "__main__":
    main()