#!/usr/bin/env python3
"""
Hermes综合技能集成系统 - 主入口
整合了技能创建、记忆系统、代理编排和技能市场功能
"""

import sys
import os
import argparse
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

# 添加脚本目录到Python路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

try:
    from scripts.skill_creator import HermesSkillCreator
    from scripts.memory_system import HermesMemory, HermesMemoryManager
    from scripts.agent_orchestrator import AgentOrchestrator, AgentType, create_task
    from scripts.skill_marketplace import SkillMarketplace, SkillPublisher
except ImportError as e:
    print(f"警告: 导入模块失败 - {e}")
    # 尝试添加脚本目录到路径
    script_dir = Path(__file__).parent / "scripts"
    sys.path.insert(0, str(script_dir))
    try:
        from skill_creator import HermesSkillCreator
        from memory_system import HermesMemory, HermesMemoryManager
        from agent_orchestrator import AgentOrchestrator, AgentType, create_task
        from skill_marketplace import SkillMarketplace, SkillPublisher
    except ImportError as e2:
        print(f"再次导入失败: {e2}")
        print("某些功能可能不可用")


class HermesIntegratedSystem:
    """Hermes综合技能集成系统"""
    
    def __init__(self, config_path: Optional[str] = None):
        # 加载配置
        self.config = self._load_config(config_path)
        
        # 初始化组件
        self.skill_creator = None
        self.memory_manager = None
        self.agent_orchestrator = None
        self.skill_marketplace = None
        
        # 初始化系统
        self._initialize_system()
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """加载配置文件"""
        if not config_path:
            config_path = script_dir / "config.yaml"
        
        config_path = Path(config_path)
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            # 返回默认配置
            return {
                'system': {
                    'name': 'Hermes综合技能集成系统',
                    'version': '1.0.0'
                },
                'performance': {
                    'max_workers': 4,
                    'cache_size': 1000
                }
            }
    
    def _initialize_system(self):
        """初始化系统组件"""
        print(f"正在初始化 {self.config['system']['name']} v{self.config['system']['version']}")
        
        try:
            # 初始化技能创建器
            self.skill_creator = HermesSkillCreator()
            print("✅ 技能创建器初始化完成")
        except Exception as e:
            print(f"⚠️ 技能创建器初始化失败: {e}")
        
        try:
            # 初始化记忆管理器
            self.memory_manager = HermesMemoryManager()
            print("✅ 记忆管理器初始化完成")
        except Exception as e:
            print(f"⚠️ 记忆管理器初始化失败: {e}")
        
        try:
            # 初始化代理编排器
            max_workers = self.config.get('performance', {}).get('max_workers', 4)
            self.agent_orchestrator = AgentOrchestrator(max_workers=max_workers)
            print("✅ 代理编排器初始化完成")
        except Exception as e:
            print(f"⚠️ 代理编排器初始化失败: {e}")
        
        try:
            # 初始化技能市场
            self.skill_marketplace = SkillMarketplace()
            print("✅ 技能市场初始化完成")
        except Exception as e:
            print(f"⚠️ 技能市场初始化失败: {e}")
        
        print("🚀 系统初始化完成！")
    
    def create_skill(self, description: str, skill_name: Optional[str] = None) -> Dict[str, Any]:
        """创建技能"""
        if not self.skill_creator:
            return {'success': False, 'error': '技能创建器未初始化'}
        
        try:
            result = self.skill_creator.create_skill_from_description(description, skill_name)
            
            # 保存到记忆
            if self.memory_manager:
                self.memory_manager.save_skill_knowledge(
                    skill_name=result['skill_name'],
                    knowledge={
                        'description': description,
                        'creation_date': result.get('creation_date', ''),
                        'files_created': result.get('files_created', [])
                    }
                )
            
            return {'success': True, 'result': result}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def search_memories(self, query: str, category: Optional[str] = None) -> Dict[str, Any]:
        """搜索记忆"""
        if not self.memory_manager:
            return {'success': False, 'error': '记忆管理器未初始化'}
        
        try:
            results = self.memory_manager.memory.search(query, category)
            return {'success': True, 'results': results}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def execute_agent_task(self, description: str, agent_type: str) -> Dict[str, Any]:
        """执行代理任务"""
        if not self.agent_orchestrator:
            return {'success': False, 'error': '代理编排器未初始化'}
        
        try:
            # 创建任务
            task = create_task(description, agent_type)
            
            # 添加任务到队列
            self.agent_orchestrator.add_task(task)
            
            # 执行任务
            import asyncio
            result = asyncio.run(self.agent_orchestrator.execute_task(task))
            
            # 保存结果到记忆
            if self.memory_manager and result.success:
                self.memory_manager.save_conversation_insight(
                    topic=f"agent_task_{task.id}",
                    insight=f"任务完成: {description}",
                    importance="medium"
                )
            
            return {
                'success': True,
                'result': result.to_dict()
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def search_skills(self, query: str, category: Optional[str] = None) -> Dict[str, Any]:
        """搜索技能"""
        if not self.skill_marketplace:
            return {'success': False, 'error': '技能市场未初始化'}
        
        try:
            results = self.skill_marketplace.search_skills(query, category)
            return {'success': True, 'results': results}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def install_skill(self, skill_name: str, source: str = 'local') -> Dict[str, Any]:
        """安装技能"""
        if not self.skill_marketplace:
            return {'success': False, 'error': '技能市场未初始化'}
        
        try:
            result = self.skill_marketplace.install_skill(skill_name, source)
            
            # 保存到记忆
            if self.memory_manager and result['success']:
                self.memory_manager.save_skill_knowledge(
                    skill_name=skill_name,
                    knowledge={
                        'source': source,
                        'install_date': result.get('install_date', ''),
                        'install_path': result.get('install_path', '')
                    }
                )
            
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        status = {
            'system': {
                'name': self.config['system']['name'],
                'version': self.config['system']['version'],
                'components': {}
            }
        }
        
        # 检查组件状态
        components = {
            'skill_creator': self.skill_creator,
            'memory_manager': self.memory_manager,
            'agent_orchestrator': self.agent_orchestrator,
            'skill_marketplace': self.skill_marketplace
        }
        
        for name, component in components.items():
            status['system']['components'][name] = {
                'available': component is not None,
                'status': 'active' if component else 'inactive'
            }
        
        # 获取统计信息
        if self.memory_manager:
            try:
                memory_stats = self.memory_manager.memory.get_stats()
                status['memory'] = memory_stats
            except:
                pass
        
        if self.agent_orchestrator:
            try:
                agent_stats = self.agent_orchestrator.get_statistics()
                status['agents'] = agent_stats
            except:
                pass
        
        if self.skill_marketplace:
            try:
                marketplace_stats = self.skill_marketplace.get_statistics()
                status['marketplace'] = marketplace_stats
            except:
                pass
        
        return status
    
    def save_user_preference(self, key: str, value: Any, description: Optional[str] = None):
        """保存用户偏好"""
        if self.memory_manager:
            self.memory_manager.save_user_preference(key, value, description)
    
    def get_user_preferences(self) -> Dict[str, Any]:
        """获取用户偏好"""
        if self.memory_manager:
            return self.memory_manager.get_user_preferences()
        return {}


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='Hermes综合技能集成系统')
    parser.add_argument('action', choices=[
        'status', 'create-skill', 'search-memories', 'execute-agent',
        'search-skills', 'install-skill', 'save-preference', 'get-preferences'
    ])
    parser.add_argument('--description', '-d', help='描述')
    parser.add_argument('--name', '-n', help='名称')
    parser.add_argument('--query', '-q', help='查询')
    parser.add_argument('--category', '-c', help='类别')
    parser.add_argument('--agent', '-a', help='代理类型')
    parser.add_argument('--source', '-s', default='local', help='技能源')
    parser.add_argument('--key', '-k', help='键')
    parser.add_argument('--value', '-v', help='值')
    parser.add_argument('--config', help='配置文件路径')
    
    args = parser.parse_args()
    
    # 初始化系统
    system = HermesIntegratedSystem(args.config)
    
    if args.action == 'status':
        status = system.get_system_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
    
    elif args.action == 'create-skill':
        if not args.description:
            print("错误: 需要提供 --description")
            return
        
        result = system.create_skill(args.description, args.name)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'search-memories':
        if not args.query:
            print("错误: 需要提供 --query")
            return
        
        result = system.search_memories(args.query, args.category)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'execute-agent':
        if not args.description or not args.agent:
            print("错误: 需要提供 --description 和 --agent")
            return
        
        result = system.execute_agent_task(args.description, args.agent)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'search-skills':
        if not args.query:
            print("错误: 需要提供 --query")
            return
        
        result = system.search_skills(args.query, args.category)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'install-skill':
        if not args.name:
            print("错误: 需要提供 --name")
            return
        
        result = system.install_skill(args.name, args.source)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.action == 'save-preference':
        if not args.key or not args.value:
            print("错误: 需要提供 --key 和 --value")
            return
        
        system.save_user_preference(args.key, args.value, args.description)
        print(f"偏好已保存: {args.key}")
    
    elif args.action == 'get-preferences':
        preferences = system.get_user_preferences()
        print(json.dumps(preferences, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()