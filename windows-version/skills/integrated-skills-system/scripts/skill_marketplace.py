#!/usr/bin/env python3
"""
Hermes技能市场系统 - 基于buildwithclaude的学习成果
为Hermes Agent提供技能发现、安装、更新和分享功能
"""

import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging
import subprocess
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SkillMarketplace:
    """技能市场类 - 管理技能的发现、安装和更新"""
    
    def __init__(self, skills_dir: str = "~/.hermes/skills", 
                 cache_dir: str = "~/.hermes/cache/skills"):
        self.skills_dir = Path(skills_dir).expanduser()
        self.cache_dir = Path(cache_dir).expanduser()
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 技能注册表
        self.registry_path = self.skills_dir / "registry.json"
        self.registry = self._load_registry()
        
        # 市场源
        self.marketplaces = {
            'local': '本地技能库',
            'github': 'GitHub技能库',
            'community': '社区技能库'
        }
    
    def _load_registry(self) -> Dict[str, Any]:
        """加载技能注册表"""
        if self.registry_path.exists():
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'skills': {}, 'marketplaces': {}, 'last_updated': None}
    
    def _save_registry(self):
        """保存技能注册表"""
        self.registry['last_updated'] = datetime.now().isoformat()
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(self.registry, f, ensure_ascii=False, indent=2)
    
    def search_skills(self, query: str, category: Optional[str] = None, 
                     limit: int = 20) -> List[Dict[str, Any]]:
        """
        搜索技能
        
        Args:
            query: 搜索查询
            category: 技能类别（可选）
            limit: 返回结果数量限制
            
        Returns:
            技能列表
        """
        results = []
        query_lower = query.lower()
        
        # 搜索本地已安装技能
        for skill_name, skill_info in self.registry['skills'].items():
            # 检查类别
            if category and skill_info.get('category') != category:
                continue
            
            # 检查匹配度
            score = self._calculate_match_score(query_lower, skill_info)
            if score > 0:
                results.append({
                    'name': skill_name,
                    'description': skill_info.get('description', ''),
                    'category': skill_info.get('category', 'uncategorized'),
                    'version': skill_info.get('version', '1.0.0'),
                    'author': skill_info.get('author', 'Unknown'),
                    'tags': skill_info.get('tags', []),
                    'installed': True,
                    'score': score,
                    'source': 'local'
                })
        
        # 搜索远程技能（模拟）
        remote_skills = self._search_remote_skills(query_lower, category)
        results.extend(remote_skills)
        
        # 按匹配度排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:limit]
    
    def _calculate_match_score(self, query: str, skill_info: Dict[str, Any]) -> float:
        """计算匹配度分数"""
        score = 0.0
        
        # 检查名称匹配
        name = skill_info.get('name', '').lower()
        if query in name:
            score += 10.0
        elif name in query:
            score += 5.0
        
        # 检查描述匹配
        description = skill_info.get('description', '').lower()
        if query in description:
            score += 3.0
        
        # 检查标签匹配
        tags = skill_info.get('tags', [])
        for tag in tags:
            if query in tag.lower():
                score += 2.0
        
        # 检查类别匹配
        category = skill_info.get('category', '').lower()
        if query in category:
            score += 1.0
        
        return score
    
    def _search_remote_skills(self, query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """搜索远程技能（模拟实现）"""
        # 在实际应用中，这里会调用远程API
        # 现在返回模拟数据
        mock_skills = [
            {
                'name': 'data-converter',
                'description': '数据格式转换工具，支持JSON、CSV、XML等格式',
                'category': 'data-processing',
                'version': '1.2.0',
                'author': 'Hermes Community',
                'tags': ['data', 'convert', 'json', 'csv'],
                'installed': False,
                'score': 5.0,
                'source': 'github',
                'download_url': 'https://github.com/hermes-skills/data-converter'
            },
            {
                'name': 'api-tester',
                'description': 'API测试工具，支持REST和GraphQL接口测试',
                'category': 'testing',
                'version': '2.1.0',
                'author': 'API Experts',
                'tags': ['api', 'test', 'rest', 'graphql'],
                'installed': False,
                'score': 4.5,
                'source': 'community',
                'download_url': 'https://github.com/hermes-skills/api-tester'
            },
            {
                'name': 'image-optimizer',
                'description': '图片优化工具，支持压缩、格式转换、尺寸调整',
                'category': 'media',
                'version': '1.5.0',
                'author': 'Media Team',
                'tags': ['image', 'optimize', 'compress', 'resize'],
                'installed': False,
                'score': 4.0,
                'source': 'github',
                'download_url': 'https://github.com/hermes-skills/image-optimizer'
            },
            {
                'name': 'code-formatter',
                'description': '代码格式化工具，支持多种编程语言',
                'category': 'development',
                'version': '3.0.0',
                'author': 'Dev Tools',
                'tags': ['code', 'format', 'lint', 'style'],
                'installed': False,
                'score': 3.5,
                'source': 'community',
                'download_url': 'https://github.com/hermes-skills/code-formatter'
            },
            {
                'name': 'db-migration',
                'description': '数据库迁移工具，支持Schema版本控制',
                'category': 'database',
                'version': '1.8.0',
                'author': 'DB Admins',
                'tags': ['database', 'migration', 'schema', 'version'],
                'installed': False,
                'score': 3.0,
                'source': 'github',
                'download_url': 'https://github.com/hermes-skills/db-migration'
            }
        ]
        
        # 过滤结果
        results = []
        for skill in mock_skills:
            if category and skill['category'] != category:
                continue
            
            score = self._calculate_match_score(query, skill)
            if score > 0:
                skill['score'] = score
                results.append(skill)
        
        return results
    
    def install_skill(self, skill_name: str, source: str = 'local', 
                     version: Optional[str] = None) -> Dict[str, Any]:
        """
        安装技能
        
        Args:
            skill_name: 技能名称
            source: 技能源
            version: 指定版本
            
        Returns:
            安装结果
        """
        logger.info(f"开始安装技能: {skill_name} (源: {source})")
        
        # 检查是否已安装
        if skill_name in self.registry['skills']:
            logger.warning(f"技能已安装: {skill_name}")
            return {
                'success': False,
                'message': f'技能已安装: {skill_name}',
                'skill_name': skill_name
            }
        
        # 创建技能目录
        skill_dir = self.skills_dir / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            if source == 'local':
                # 从本地安装
                success = self._install_from_local(skill_name, skill_dir, version)
            elif source == 'github':
                # 从GitHub安装
                success = self._install_from_github(skill_name, skill_dir, version)
            elif source == 'community':
                # 从社区安装
                success = self._install_from_community(skill_name, skill_dir, version)
            else:
                raise ValueError(f"不支持的源: {source}")
            
            if success:
                # 注册技能
                self._register_skill(skill_name, skill_dir, source)
                
                logger.info(f"技能安装成功: {skill_name}")
                return {
                    'success': True,
                    'message': f'技能安装成功: {skill_name}',
                    'skill_name': skill_name,
                    'install_path': str(skill_dir)
                }
            else:
                raise Exception("安装失败")
                
        except Exception as e:
            # 清理失败的安装
            if skill_dir.exists():
                shutil.rmtree(skill_dir)
            
            logger.error(f"技能安装失败: {skill_name} - {e}")
            return {
                'success': False,
                'message': f'技能安装失败: {e}',
                'skill_name': skill_name,
                'error': str(e)
            }
    
    def _install_from_local(self, skill_name: str, skill_dir: Path, 
                           version: Optional[str]) -> bool:
        """从本地安装技能"""
        # 在实际应用中，这里会从本地库复制技能
        # 现在创建模拟的技能文件
        
        # 创建SKILL.md
        skill_md = f"""---
name: {skill_name}
description: 本地安装的技能
version: {version or '1.0.0'}
author: Hermes Agent
license: MIT
---

# {skill_name.replace('-', ' ').title()}

这是通过Hermes技能市场安装的本地技能。

## 使用方法

```python
# 在Hermes Agent中使用
/hermes-skill {skill_name}
```
"""
        
        (skill_dir / "SKILL.md").write_text(skill_md, encoding='utf-8')
        
        # 创建README.md
        readme = f"""# {skill_name}

本地安装的技能。

## 安装信息

- 安装时间: {datetime.now().isoformat()}
- 安装源: local
- 版本: {version or '1.0.0'}

## 使用方法

查看SKILL.md获取详细使用说明。
"""
        
        (skill_dir / "README.md").write_text(readme, encoding='utf-8')
        
        return True
    
    def _install_from_github(self, skill_name: str, skill_dir: Path, 
                            version: Optional[str]) -> bool:
        """从GitHub安装技能"""
        try:
            # 模拟从GitHub克隆
            # 在实际应用中，这里会使用git clone
            logger.info(f"从GitHub克隆技能: {skill_name}")
            
            # 创建模拟的技能文件
            return self._install_from_local(skill_name, skill_dir, version)
            
        except Exception as e:
            logger.error(f"从GitHub安装失败: {e}")
            return False
    
    def _install_from_community(self, skill_name: str, skill_dir: Path, 
                               version: Optional[str]) -> bool:
        """从社区安装技能"""
        try:
            # 模拟从社区下载
            logger.info(f"从社区下载技能: {skill_name}")
            
            # 创建模拟的技能文件
            return self._install_from_local(skill_name, skill_dir, version)
            
        except Exception as e:
            logger.error(f"从社区安装失败: {e}")
            return False
    
    def _register_skill(self, skill_name: str, skill_dir: Path, source: str):
        """注册技能到注册表"""
        # 读取SKILL.md获取技能信息
        skill_md_path = skill_dir / "SKILL.md"
        skill_info = {
            'name': skill_name,
            'description': '技能描述',
            'category': 'uncategorized',
            'version': '1.0.0',
            'author': 'Unknown',
            'tags': [],
            'install_path': str(skill_dir),
            'source': source,
            'installed_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        # 如果SKILL.md存在，尝试解析
        if skill_md_path.exists():
            try:
                with open(skill_md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 简单解析YAML头部
                if content.startswith('---'):
                    yaml_end = content.find('---', 3)
                    if yaml_end != -1:
                        yaml_content = content[3:yaml_end].strip()
                        # 这里可以添加YAML解析逻辑
                        
            except Exception as e:
                logger.warning(f"解析SKILL.md失败: {e}")
        
        self.registry['skills'][skill_name] = skill_info
        self._save_registry()
    
    def uninstall_skill(self, skill_name: str) -> Dict[str, Any]:
        """卸载技能"""
        logger.info(f"开始卸载技能: {skill_name}")
        
        if skill_name not in self.registry['skills']:
            return {
                'success': False,
                'message': f'技能未安装: {skill_name}',
                'skill_name': skill_name
            }
        
        try:
            # 获取技能目录
            skill_info = self.registry['skills'][skill_name]
            skill_dir = Path(skill_info['install_path'])
            
            # 删除技能目录
            if skill_dir.exists():
                shutil.rmtree(skill_dir)
            
            # 从注册表移除
            del self.registry['skills'][skill_name]
            self._save_registry()
            
            logger.info(f"技能卸载成功: {skill_name}")
            return {
                'success': True,
                'message': f'技能卸载成功: {skill_name}',
                'skill_name': skill_name
            }
            
        except Exception as e:
            logger.error(f"技能卸载失败: {skill_name} - {e}")
            return {
                'success': False,
                'message': f'技能卸载失败: {e}',
                'skill_name': skill_name,
                'error': str(e)
            }
    
    def update_skill(self, skill_name: str) -> Dict[str, Any]:
        """更新技能"""
        logger.info(f"开始更新技能: {skill_name}")
        
        if skill_name not in self.registry['skills']:
            return {
                'success': False,
                'message': f'技能未安装: {skill_name}',
                'skill_name': skill_name
            }
        
        try:
            # 获取技能信息
            skill_info = self.registry['skills'][skill_name]
            source = skill_info['source']
            
            # 先卸载
            self.uninstall_skill(skill_name)
            
            # 重新安装
            result = self.install_skill(skill_name, source)
            
            if result['success']:
                logger.info(f"技能更新成功: {skill_name}")
                return {
                    'success': True,
                    'message': f'技能更新成功: {skill_name}',
                    'skill_name': skill_name
                }
            else:
                raise Exception(result.get('message', '更新失败'))
                
        except Exception as e:
            logger.error(f"技能更新失败: {skill_name} - {e}")
            return {
                'success': False,
                'message': f'技能更新失败: {e}',
                'skill_name': skill_name,
                'error': str(e)
            }
    
    def list_installed_skills(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出已安装的技能"""
        skills = []
        
        for skill_name, skill_info in self.registry['skills'].items():
            if category and skill_info.get('category') != category:
                continue
            
            skills.append({
                'name': skill_name,
                'description': skill_info.get('description', ''),
                'category': skill_info.get('category', 'uncategorized'),
                'version': skill_info.get('version', '1.0.0'),
                'author': skill_info.get('author', 'Unknown'),
                'tags': skill_info.get('tags', []),
                'installed_at': skill_info.get('installed_at', ''),
                'source': skill_info.get('source', 'local')
            })
        
        return sorted(skills, key=lambda x: x['name'])
    
    def get_skill_details(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """获取技能详情"""
        if skill_name not in self.registry['skills']:
            return None
        
        skill_info = self.registry['skills'][skill_name].copy()
        
        # 添加额外信息
        skill_dir = Path(skill_info['install_path'])
        if skill_dir.exists():
            # 检查文件大小
            total_size = 0
            file_count = 0
            
            for file_path in skill_dir.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
                    file_count += 1
            
            skill_info['total_size'] = total_size
            skill_info['file_count'] = file_count
            skill_info['is_valid'] = (skill_dir / "SKILL.md").exists()
        
        return skill_info
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """获取技能类别"""
        categories = {}
        
        for skill_info in self.registry['skills'].values():
            category = skill_info.get('category', 'uncategorized')
            if category not in categories:
                categories[category] = {
                    'name': category,
                    'count': 0,
                    'skills': []
                }
            
            categories[category]['count'] += 1
            categories[category]['skills'].append(skill_info['name'])
        
        return sorted(categories.values(), key=lambda x: x['count'], reverse=True)
    
    def backup_skills(self, backup_path: Optional[str] = None) -> str:
        """备份所有技能"""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = str(self.cache_dir / f"backup_{timestamp}.tar.gz")
        
        backup_file = Path(backup_path)
        backup_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # 创建临时目录
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # 复制技能目录
                backup_skills_dir = temp_path / "skills"
                if self.skills_dir.exists():
                    shutil.copytree(self.skills_dir, backup_skills_dir)
                
                # 复制注册表
                if self.registry_path.exists():
                    shutil.copy2(self.registry_path, temp_path / "registry.json")
                
                # 创建压缩包
                shutil.make_archive(
                    str(backup_file.with_suffix('')),
                    'gztar',
                    temp_dir
                )
            
            logger.info(f"技能备份完成: {backup_file}")
            return str(backup_file)
            
        except Exception as e:
            logger.error(f"技能备份失败: {e}")
            raise
    
    def restore_skills(self, backup_path: str) -> bool:
        """恢复技能"""
        backup_file = Path(backup_path)
        
        if not backup_file.exists():
            logger.error(f"备份文件不存在: {backup_path}")
            return False
        
        try:
            # 创建临时目录
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # 解压备份文件
                shutil.unpack_archive(str(backup_file), str(temp_path))
                
                # 恢复技能目录
                backup_skills_dir = temp_path / "skills"
                if backup_skills_dir.exists():
                    if self.skills_dir.exists():
                        shutil.rmtree(self.skills_dir)
                    shutil.copytree(backup_skills_dir, self.skills_dir)
                
                # 恢复注册表
                backup_registry = temp_path / "registry.json"
                if backup_registry.exists():
                    shutil.copy2(backup_registry, self.registry_path)
            
            # 重新加载注册表
            self.registry = self._load_registry()
            
            logger.info(f"技能恢复完成: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"技能恢复失败: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        total_skills = len(self.registry['skills'])
        
        # 按类别统计
        categories = {}
        for skill_info in self.registry['skills'].values():
            category = skill_info.get('category', 'uncategorized')
            categories[category] = categories.get(category, 0) + 1
        
        # 按源统计
        sources = {}
        for skill_info in self.registry['skills'].values():
            source = skill_info.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        return {
            'total_skills': total_skills,
            'categories': categories,
            'sources': sources,
            'last_updated': self.registry.get('last_updated', 'never')
        }


class SkillPublisher:
    """技能发布器 - 用于发布自定义技能到市场"""
    
    def __init__(self, marketplace: SkillMarketplace):
        self.marketplace = marketplace
    
    def publish_skill(self, skill_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        发布技能
        
        Args:
            skill_path: 技能路径
            metadata: 技能元数据
            
        Returns:
            发布结果
        """
        skill_dir = Path(skill_path)
        
        if not skill_dir.exists():
            return {
                'success': False,
                'message': f'技能目录不存在: {skill_path}'
            }
        
        # 验证技能
        validation_result = self._validate_skill(skill_dir)
        if not validation_result['valid']:
            return {
                'success': False,
                'message': f'技能验证失败: {validation_result["errors"]}'
            }
        
        # 准备发布包
        try:
            package_path = self._create_package(skill_dir, metadata)
            
            # 发布到市场（模拟）
            logger.info(f"技能发布成功: {metadata.get('name', 'unknown')}")
            
            return {
                'success': True,
                'message': '技能发布成功',
                'package_path': str(package_path),
                'skill_name': metadata.get('name', 'unknown')
            }
            
        except Exception as e:
            logger.error(f"技能发布失败: {e}")
            return {
                'success': False,
                'message': f'技能发布失败: {e}',
                'error': str(e)
            }
    
    def _validate_skill(self, skill_dir: Path) -> Dict[str, Any]:
        """验证技能"""
        errors = []
        
        # 检查必需文件
        required_files = ['SKILL.md']
        for file_name in required_files:
            if not (skill_dir / file_name).exists():
                errors.append(f'缺少必需文件: {file_name}')
        
        # 检查SKILL.md格式
        skill_md_path = skill_dir / "SKILL.md"
        if skill_md_path.exists():
            try:
                with open(skill_md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if not content.startswith('---'):
                    errors.append('SKILL.md格式错误: 缺少YAML头部')
                
            except Exception as e:
                errors.append(f'读取SKILL.md失败: {e}')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def _create_package(self, skill_dir: Path, metadata: Dict[str, Any]) -> Path:
        """创建发布包"""
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # 复制技能文件
            package_dir = temp_path / metadata['name']
            shutil.copytree(skill_dir, package_dir)
            
            # 添加发布元数据
            publish_metadata = {
                'name': metadata['name'],
                'version': metadata.get('version', '1.0.0'),
                'description': metadata.get('description', ''),
                'author': metadata.get('author', 'Unknown'),
                'license': metadata.get('license', 'MIT'),
                'published_at': datetime.now().isoformat(),
                'category': metadata.get('category', 'uncategorized'),
                'tags': metadata.get('tags', [])
            }
            
            metadata_path = package_dir / "publish_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(publish_metadata, f, ensure_ascii=False, indent=2)
            
            # 创建压缩包
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            package_path = self.marketplace.cache_dir / f"{metadata['name']}_{timestamp}.tar.gz"
            
            shutil.make_archive(
                str(package_path.with_suffix('')),
                'gztar',
                temp_path
            )
        
        return package_path


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Hermes技能市场')
    parser.add_argument('action', choices=['search', 'install', 'uninstall', 'update', 'list', 'info', 'stats', 'backup', 'restore'])
    parser.add_argument('--query', '-q', help='搜索查询')
    parser.add_argument('--skill', '-s', help='技能名称')
    parser.add_argument('--source', default='local', help='技能源')
    parser.add_argument('--category', '-c', help='技能类别')
    parser.add_argument('--backup-path', help='备份文件路径')
    
    args = parser.parse_args()
    
    marketplace = SkillMarketplace()
    
    if args.action == 'search':
        if not args.query:
            print("错误: 需要提供 --query")
            return
        
        results = marketplace.search_skills(args.query, args.category)
        print(f"找到 {len(results)} 个技能:")
        for skill in results:
            print(f"  {skill['name']} ({skill['category']}) - {skill['description'][:50]}...")
            print(f"    版本: {skill['version']} | 作者: {skill['author']} | 安装: {'是' if skill['installed'] else '否'}")
    
    elif args.action == 'install':
        if not args.skill:
            print("错误: 需要提供 --skill")
            return
        
        result = marketplace.install_skill(args.skill, args.source)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'uninstall':
        if not args.skill:
            print("错误: 需要提供 --skill")
            return
        
        result = marketplace.uninstall_skill(args.skill)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'update':
        if not args.skill:
            print("错误: 需要提供 --skill")
            return
        
        result = marketplace.update_skill(args.skill)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'list':
        skills = marketplace.list_installed_skills(args.category)
        print(f"已安装 {len(skills)} 个技能:")
        for skill in skills:
            print(f"  {skill['name']} ({skill['category']}) - {skill['description'][:50]}...")
            print(f"    版本: {skill['version']} | 作者: {skill['author']} | 源: {skill['source']}")
    
    elif args.action == 'info':
        if not args.skill:
            print("错误: 需要提供 --skill")
            return
        
        details = marketplace.get_skill_details(args.skill)
        if details:
            print(json.dumps(details, ensure_ascii=False, indent=2))
        else:
            print(f"技能未找到: {args.skill}")
    
    elif args.action == 'stats':
        stats = marketplace.get_statistics()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    elif args.action == 'backup':
        backup_path = marketplace.backup_skills(args.backup_path)
        print(f"备份完成: {backup_path}")
    
    elif args.action == 'restore':
        if not args.backup_path:
            print("错误: 需要提供 --backup-path")
            return
        
        if marketplace.restore_skills(args.backup_path):
            print("恢复完成")
        else:
            print("恢复失败")


if __name__ == '__main__':
    main()