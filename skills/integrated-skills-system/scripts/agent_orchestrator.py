#!/usr/bin/env python3
"""
Hermes代理编排系统 - 基于everything-claude-code的学习成果
为Hermes Agent提供专业代理调度、并行执行和错误处理功能
"""

import json
import asyncio
import concurrent.futures
from typing import Dict, List, Any, Optional, Callable, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentType(Enum):
    """代理类型枚举"""
    PLANNER = "planner"           # 规划代理
    ARCHITECT = "architect"       # 架构代理
    TDD_GUIDE = "tdd-guide"       # TDD代理
    CODE_REVIEWER = "code-reviewer"  # 代码审查代理
    SECURITY_REVIEWER = "security-reviewer"  # 安全审查代理
    BUILD_ERROR_RESOLVER = "build-error-resolver"  # 构建错误解决代理
    REFACTOR_CLEANER = "refactor-cleaner"  # 重构清理代理
    DOC_UPDATER = "doc-updater"   # 文档更新代理
    DEBUGGER = "debugger"         # 调试代理
    TESTING = "testing"           # 测试代理
    PERFORMANCE = "performance"   # 性能优化代理
    DATABASE = "database"         # 数据库代理
    API_DESIGNER = "api-designer" # API设计代理
    UI_DESIGNER = "ui-designer"   # UI设计代理
    DEVOPS = "devops"             # DevOps代理
    SECURITY_SCANNER = "security-scanner"  # 安全扫描代理
    DATA_ENGINEER = "data-engineer"  # 数据工程代理
    ML_ENGINEER = "ml-engineer"   # 机器学习代理
    GENERAL = "general"           # 通用代理


@dataclass
class AgentTask:
    """代理任务数据类"""
    id: str
    description: str
    agent_type: AgentType
    priority: int = 1  # 1-5，5为最高优先级
    context: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    timeout: int = 300  # 秒
    retry_count: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'description': self.description,
            'agent_type': self.agent_type.value,
            'priority': self.priority,
            'context': self.context,
            'dependencies': self.dependencies,
            'timeout': self.timeout,
            'retry_count': self.retry_count,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class AgentResult:
    """代理结果数据类"""
    task_id: str
    success: bool
    data: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    agent_type: Optional[AgentType] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'task_id': self.task_id,
            'success': self.success,
            'data': self.data,
            'error': self.error,
            'execution_time': self.execution_time,
            'agent_type': self.agent_type.value if self.agent_type else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class Agent:
    """代理基类"""
    
    def __init__(self, agent_type: AgentType, name: Optional[str] = None):
        self.agent_type = agent_type
        self.name = name or agent_type.value
        self.capabilities = []
        self.tools = []
        
    async def execute(self, task: AgentTask) -> AgentResult:
        """执行任务"""
        raise NotImplementedError("子类必须实现execute方法")
    
    def can_handle(self, task: AgentTask) -> bool:
        """检查是否能处理此任务"""
        return task.agent_type == self.agent_type
    
    def get_capabilities(self) -> List[str]:
        """获取能力列表"""
        return self.capabilities
    
    def get_tools(self) -> List[str]:
        """获取工具列表"""
        return self.tools


class PlannerAgent(Agent):
    """规划代理 - 负责实现规划和任务分解"""
    
    def __init__(self):
        super().__init__(AgentType.PLANNER, "规划代理")
        self.capabilities = [
            "任务分解",
            "依赖分析",
            "优先级排序",
            "资源规划",
            "风险评估"
        ]
        self.tools = ["task_analyzer", "dependency_graph", "resource_planner"]
    
    async def execute(self, task: AgentTask) -> AgentResult:
        """执行规划任务"""
        start_time = datetime.now()
        
        try:
            description = task.description
            context = task.context
            
            # 分析任务
            analysis = self._analyze_task(description, context)
            
            # 生成计划
            plan = self._generate_plan(analysis)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                task_id=task.id,
                success=True,
                data=plan,
                execution_time=execution_time,
                agent_type=self.agent_type,
                started_at=start_time,
                completed_at=datetime.now()
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return AgentResult(
                task_id=task.id,
                success=False,
                error=str(e),
                execution_time=execution_time,
                agent_type=self.agent_type,
                started_at=start_time,
                completed_at=datetime.now()
            )
    
    def _analyze_task(self, description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """分析任务"""
        # 简化的任务分析
        return {
            'description': description,
            'complexity': self._estimate_complexity(description),
            'dependencies': self._identify_dependencies(description),
            'resources_needed': self._identify_resources(description),
            'risks': self._identify_risks(description)
        }
    
    def _estimate_complexity(self, description: str) -> str:
        """估计复杂性"""
        word_count = len(description.split())
        if word_count < 20:
            return "low"
        elif word_count < 50:
            return "medium"
        else:
            return "high"
    
    def _identify_dependencies(self, description: str) -> List[str]:
        """识别依赖"""
        dependencies = []
        if "api" in description.lower():
            dependencies.append("api_access")
        if "database" in description.lower():
            dependencies.append("database_connection")
        if "file" in description.lower():
            dependencies.append("file_system")
        return dependencies
    
    def _identify_resources(self, description: str) -> List[str]:
        """识别资源需求"""
        resources = []
        if "image" in description.lower() or "photo" in description.lower():
            resources.append("image_processing")
        if "data" in description.lower():
            resources.append("data_processing")
        if "network" in description.lower() or "internet" in description.lower():
            resources.append("network_access")
        return resources
    
    def _identify_risks(self, description: str) -> List[str]:
        """识别风险"""
        risks = []
        if "security" in description.lower():
            risks.append("security_risk")
        if "performance" in description.lower():
            risks.append("performance_risk")
        if "data" in description.lower() and "loss" in description.lower():
            risks.append("data_loss_risk")
        return risks
    
    def _generate_plan(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """生成计划"""
        return {
            'plan': {
                'phases': [
                    {
                        'name': '准备阶段',
                        'tasks': ['环境检查', '依赖安装', '资源准备']
                    },
                    {
                        'name': '实现阶段',
                        'tasks': ['核心功能实现', '错误处理', '测试']
                    },
                    {
                        'name': '完成阶段',
                        'tasks': ['代码审查', '文档更新', '部署']
                    }
                ],
                'estimated_time': self._estimate_time(analysis['complexity']),
                'resources_needed': analysis['resources_needed'],
                'risks': analysis['risks']
            }
        }
    
    def _estimate_time(self, complexity: str) -> str:
        """估计时间"""
        if complexity == "low":
            return "1-2小时"
        elif complexity == "medium":
            return "4-8小时"
        else:
            return "1-3天"


class CodeReviewerAgent(Agent):
    """代码审查代理 - 负责代码质量和可维护性"""
    
    def __init__(self):
        super().__init__(AgentType.CODE_REVIEWER, "代码审查代理")
        self.capabilities = [
            "代码质量检查",
            "风格一致性检查",
            "性能优化建议",
            "安全漏洞检测",
            "重构建议"
        ]
        self.tools = ["static_analyzer", "linter", "security_scanner"]
    
    async def execute(self, task: AgentTask) -> AgentResult:
        """执行代码审查任务"""
        start_time = datetime.now()
        
        try:
            code = task.context.get('code', '')
            language = task.context.get('language', 'python')
            
            # 执行代码审查
            review_result = self._review_code(code, language)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                task_id=task.id,
                success=True,
                data=review_result,
                execution_time=execution_time,
                agent_type=self.agent_type,
                started_at=start_time,
                completed_at=datetime.now()
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return AgentResult(
                task_id=task.id,
                success=False,
                error=str(e),
                execution_time=execution_time,
                agent_type=self.agent_type,
                started_at=start_time,
                completed_at=datetime.now()
            )
    
    def _review_code(self, code: str, language: str) -> Dict[str, Any]:
        """审查代码"""
        # 简化的代码审查
        issues = []
        suggestions = []
        
        # 检查代码长度
        lines = code.split('\n')
        if len(lines) > 100:
            issues.append({
                'type': 'style',
                'severity': 'medium',
                'message': '函数过长，建议拆分',
                'line': 100
            })
        
        # 检查复杂度
        if code.count('if') > 5:
            issues.append({
                'type': 'complexity',
                'severity': 'high',
                'message': '条件分支过多，建议重构'
            })
        
        # 检查安全问题
        if 'eval(' in code:
            issues.append({
                'type': 'security',
                'severity': 'critical',
                'message': '使用eval可能存在安全风险'
            })
        
        if 'exec(' in code:
            issues.append({
                'type': 'security',
                'severity': 'critical',
                'message': '使用exec可能存在安全风险'
            })
        
        # 生成建议
        suggestions.append("建议添加更多注释")
        suggestions.append("考虑添加类型提示")
        suggestions.append("建议添加单元测试")
        
        return {
            'score': max(0, 100 - len(issues) * 10),
            'issues': issues,
            'suggestions': suggestions,
            'metrics': {
                'lines_of_code': len(lines),
                'complexity': self._calculate_complexity(code),
                'maintainability': self._calculate_maintainability(code)
            }
        }
    
    def _calculate_complexity(self, code: str) -> int:
        """计算复杂度"""
        complexity = 1
        complexity += code.count('if')
        complexity += code.count('for')
        complexity += code.count('while')
        complexity += code.count('switch')
        complexity += code.count('case')
        return complexity
    
    def _calculate_maintainability(self, code: str) -> float:
        """计算可维护性指数"""
        lines = code.split('\n')
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        total_lines = len(lines)
        
        if total_lines == 0:
            return 0.0
        
        comment_ratio = comment_lines / total_lines
        return min(100, comment_ratio * 500 + 50)


class SecurityReviewerAgent(Agent):
    """安全审查代理 - 负责漏洞检测"""
    
    def __init__(self):
        super().__init__(AgentType.SECURITY_REVIEWER, "安全审查代理")
        self.capabilities = [
            "漏洞扫描",
            "安全模式检查",
            "依赖安全检查",
            "配置安全检查",
            "最佳实践检查"
        ]
        self.tools = ["security_scanner", "vulnerability_db", "config_checker"]
    
    async def execute(self, task: AgentTask) -> AgentResult:
        """执行安全审查任务"""
        start_time = datetime.now()
        
        try:
            code = task.context.get('code', '')
            config = task.context.get('config', {})
            
            # 执行安全审查
            security_result = self._security_review(code, config)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                task_id=task.id,
                success=True,
                data=security_result,
                execution_time=execution_time,
                agent_type=self.agent_type,
                started_at=start_time,
                completed_at=datetime.now()
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return AgentResult(
                task_id=task.id,
                success=False,
                error=str(e),
                execution_time=execution_time,
                agent_type=self.agent_type,
                started_at=start_time,
                completed_at=datetime.now()
            )
    
    def _security_review(self, code: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """安全审查"""
        vulnerabilities = []
        warnings = []
        
        # 检查常见安全漏洞
        security_patterns = [
            (r'eval\s*\(', '代码注入风险', 'critical'),
            (r'exec\s*\(', '代码注入风险', 'critical'),
            (r'os\.system\s*\(', '命令注入风险', 'high'),
            (r'subprocess.*shell\s*=\s*True', '命令注入风险', 'high'),
            (r'password\s*=\s*["\'][^"\']+["\']', '硬编码密码', 'critical'),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', '硬编码API密钥', 'critical'),
            (r'secret\s*=\s*["\'][^"\']+["\']', '硬编码密钥', 'critical'),
            (r'pickle\.loads', '不安全的反序列化', 'high'),
            (r'yaml\.load\s*\([^)]*\)', 'YAML反序列化风险', 'medium'),
        ]
        
        for pattern, message, severity in security_patterns:
            import re
            if re.search(pattern, code, re.IGNORECASE):
                vulnerabilities.append({
                    'type': 'vulnerability',
                    'severity': severity,
                    'message': message,
                    'pattern': pattern
                })
        
        # 检查配置安全
        if config.get('debug', False):
            warnings.append({
                'type': 'warning',
                'message': '调试模式已启用，生产环境请关闭'
            })
        
        if not config.get('ssl_verify', True):
            warnings.append({
                'type': 'warning',
                'message': 'SSL验证已禁用，可能存在安全风险'
            })
        
        return {
            'security_score': max(0, 100 - len(vulnerabilities) * 20),
            'vulnerabilities': vulnerabilities,
            'warnings': warnings,
            'recommendations': [
                "使用环境变量存储敏感信息",
                "启用输入验证",
                "使用参数化查询防止SQL注入",
                "启用HTTPS",
                "定期更新依赖包"
            ]
        }


class AgentOrchestrator:
    """代理编排器 - 负责代理调度和并行执行"""
    
    def __init__(self, max_workers: int = 4):
        self.agents: Dict[AgentType, Agent] = {}
        self.task_queue: List[AgentTask] = []
        self.results: Dict[str, AgentResult] = {}
        self.max_workers = max_workers
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        
        # 注册默认代理
        self._register_default_agents()
    
    def _register_default_agents(self):
        """注册默认代理"""
        default_agents = [
            PlannerAgent(),
            CodeReviewerAgent(),
            SecurityReviewerAgent()
        ]
        
        for agent in default_agents:
            self.register_agent(agent)
    
    def register_agent(self, agent: Agent):
        """注册代理"""
        self.agents[agent.agent_type] = agent
        logger.info(f"代理已注册: {agent.name}")
    
    def get_agent(self, agent_type: AgentType) -> Optional[Agent]:
        """获取代理"""
        return self.agents.get(agent_type)
    
    def select_agent_for_task(self, task: AgentTask) -> Optional[Agent]:
        """为任务选择合适的代理"""
        # 首先检查是否有完全匹配的代理
        if task.agent_type in self.agents:
            return self.agents[task.agent_type]
        
        # 根据任务描述选择代理
        description = task.description.lower()
        
        if any(word in description for word in ['规划', '计划', '分解', 'planner']):
            return self.agents.get(AgentType.PLANNER)
        elif any(word in description for word in ['审查', '检查', 'review', 'check']):
            if any(word in description for word in ['安全', 'security', '漏洞']):
                return self.agents.get(AgentType.SECURITY_REVIEWER)
            else:
                return self.agents.get(AgentType.CODE_REVIEWER)
        elif any(word in description for word in ['测试', 'test']):
            return self.agents.get(AgentType.TESTING)
        elif any(word in description for word in ['调试', 'debug']):
            return self.agents.get(AgentType.DEBUGGER)
        elif any(word in description for word in ['重构', '优化', 'refactor']):
            return self.agents.get(AgentType.REFACTOR_CLEANER)
        elif any(word in description for word in ['文档', 'doc']):
            return self.agents.get(AgentType.DOC_UPDATER)
        else:
            return self.agents.get(AgentType.GENERAL)
    
    def add_task(self, task: AgentTask):
        """添加任务到队列"""
        self.task_queue.append(task)
        logger.info(f"任务已添加: {task.id} ({task.agent_type.value})")
    
    async def execute_task(self, task: AgentTask) -> AgentResult:
        """执行单个任务"""
        agent = self.select_agent_for_task(task)
        
        if not agent:
            return AgentResult(
                task_id=task.id,
                success=False,
                error=f"没有找到合适的代理处理任务: {task.agent_type.value}"
            )
        
        # 检查依赖
        for dep_id in task.dependencies:
            if dep_id not in self.results:
                return AgentResult(
                    task_id=task.id,
                    success=False,
                    error=f"依赖任务未完成: {dep_id}"
                )
        
        logger.info(f"开始执行任务: {task.id} 使用代理: {agent.name}")
        
        # 执行任务
        try:
            result = await agent.execute(task)
            self.results[task.id] = result
            
            if result.success:
                logger.info(f"任务完成: {task.id} (耗时: {result.execution_time:.2f}s)")
            else:
                logger.error(f"任务失败: {task.id} - {result.error}")
            
            return result
            
        except Exception as e:
            error_result = AgentResult(
                task_id=task.id,
                success=False,
                error=f"代理执行异常: {str(e)}"
            )
            self.results[task.id] = error_result
            return error_result
    
    async def execute_tasks_parallel(self, tasks: List[AgentTask]) -> List[AgentResult]:
        """并行执行多个任务"""
        logger.info(f"开始并行执行 {len(tasks)} 个任务")
        
        # 创建异步任务列表
        async_tasks = []
        for task in tasks:
            async_task = asyncio.create_task(self.execute_task(task))
            async_tasks.append(async_task)
        
        # 等待所有任务完成
        results = await asyncio.gather(*async_tasks, return_exceptions=True)
        
        # 处理结果
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                error_result = AgentResult(
                    task_id=tasks[i].id,
                    success=False,
                    error=f"任务执行异常: {str(result)}"
                )
                final_results.append(error_result)
            else:
                final_results.append(result)
        
        logger.info(f"并行执行完成: {len(final_results)} 个结果")
        return final_results
    
    def get_task_results(self, task_id: str) -> Optional[AgentResult]:
        """获取任务结果"""
        return self.results.get(task_id)
    
    def get_all_results(self) -> Dict[str, AgentResult]:
        """获取所有结果"""
        return self.results.copy()
    
    def clear_completed_tasks(self):
        """清除已完成的任务"""
        completed_tasks = [task for task in self.task_queue if task.id in self.results]
        for task in completed_tasks:
            self.task_queue.remove(task)
        
        logger.info(f"已清除 {len(completed_tasks)} 个已完成任务")
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        total_tasks = len(self.results)
        successful_tasks = sum(1 for result in self.results.values() if result.success)
        failed_tasks = total_tasks - successful_tasks
        
        total_execution_time = sum(result.execution_time for result in self.results.values())
        avg_execution_time = total_execution_time / total_tasks if total_tasks > 0 else 0
        
        agent_usage = {}
        for result in self.results.values():
            if result.agent_type:
                agent_type = result.agent_type.value
                agent_usage[agent_type] = agent_usage.get(agent_type, 0) + 1
        
        return {
            'total_tasks': total_tasks,
            'successful_tasks': successful_tasks,
            'failed_tasks': failed_tasks,
            'success_rate': successful_tasks / total_tasks if total_tasks > 0 else 0,
            'total_execution_time': total_execution_time,
            'average_execution_time': avg_execution_time,
            'agent_usage': agent_usage,
            'pending_tasks': len(self.task_queue)
        }
    
    def shutdown(self):
        """关闭执行器"""
        self.executor.shutdown(wait=True)
        logger.info("代理编排器已关闭")


# 便捷函数
def create_task(description: str, agent_type: Union[AgentType, str], 
                priority: int = 1, context: Dict[str, Any] = None,
                dependencies: List[str] = None) -> AgentTask:
    """创建任务的便捷函数"""
    if isinstance(agent_type, str):
        agent_type = AgentType(agent_type)
    
    import uuid
    task_id = str(uuid.uuid4())[:8]
    
    return AgentTask(
        id=task_id,
        description=description,
        agent_type=agent_type,
        priority=priority,
        context=context or {},
        dependencies=dependencies or []
    )


async def run_agent_orchestrator_demo():
    """代理编排器演示"""
    orchestrator = AgentOrchestrator()
    
    # 创建测试任务
    tasks = [
        create_task(
            "分析项目结构并制定实现计划",
            AgentType.PLANNER,
            context={'project_path': '/path/to/project'}
        ),
        create_task(
            "审查main.py代码质量",
            AgentType.CODE_REVIEWER,
            context={'code': 'def hello(): print("hello")', 'language': 'python'}
        ),
        create_task(
            "检查代码安全漏洞",
            AgentType.SECURITY_REVIEWER,
            context={'code': 'eval(user_input)', 'config': {'debug': True}}
        )
    ]
    
    # 添加任务到队列
    for task in tasks:
        orchestrator.add_task(task)
    
    # 并行执行任务
    results = await orchestrator.execute_tasks_parallel(tasks)
    
    # 输出结果
    print("\n任务执行结果:")
    for result in results:
        print(f"  任务 {result.task_id}: {'成功' if result.success else '失败'}")
        if result.success:
            print(f"    数据: {json.dumps(result.data, ensure_ascii=False, indent=4)}")
        else:
            print(f"    错误: {result.error}")
    
    # 输出统计信息
    stats = orchestrator.get_statistics()
    print(f"\n统计信息:")
    print(f"  总任务数: {stats['total_tasks']}")
    print(f"  成功率: {stats['success_rate']:.2%}")
    print(f"  平均执行时间: {stats['average_execution_time']:.2f}s")
    
    orchestrator.shutdown()


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Hermes代理编排系统')
    parser.add_argument('action', choices=['demo', 'stats', 'run'])
    parser.add_argument('--task', help='任务描述')
    parser.add_argument('--agent', help='代理类型')
    
    args = parser.parse_args()
    
    if args.action == 'demo':
        asyncio.run(run_agent_orchestrator_demo())
    
    elif args.action == 'stats':
        orchestrator = AgentOrchestrator()
        stats = orchestrator.get_statistics()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        orchestrator.shutdown()
    
    elif args.action == 'run':
        if not args.task or not args.agent:
            print("错误: 需要提供 --task 和 --agent")
            return
        
        orchestrator = AgentOrchestrator()
        
        try:
            agent_type = AgentType(args.agent)
        except ValueError:
            print(f"错误: 不支持的代理类型: {args.agent}")
            print(f"支持的类型: {[t.value for t in AgentType]}")
            return
        
        task = create_task(args.task, agent_type)
        result = asyncio.run(orchestrator.execute_task(task))
        
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        orchestrator.shutdown()


if __name__ == '__main__':
    main()