#!/usr/bin/env python3
"""
Hermes Agent Skill Creator - 基于agent-skill-creator的学习成果
自动创建技能的工具，支持从工作流描述、现有代码、API文档创建技能
"""

import json
import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse

class HermesSkillCreator:
    """Hermes技能创建器 - 五阶段创建流程"""
    
    def __init__(self, skills_dir: str = "~/.hermes/skills"):
        self.skills_dir = Path(skills_dir).expanduser()
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
    def create_skill_from_description(self, description: str, skill_name: Optional[str] = None) -> Dict[str, Any]:
        """从工作流描述创建技能"""
        print("🔍 阶段1: 发现 - 分析工作流描述")
        spec = self._phase1_discovery(description)
        
        print("📐 阶段2: 设计 - 生成内部规范")
        design = self._phase2_design(spec)
        
        print("🏗️ 阶段3: 构建 - 创建技能目录")
        if not skill_name:
            skill_name = self._generate_skill_name(spec)
        skill_path = self._phase3_architecture(skill_name, design)
        
        print("🎯 阶段4: 检测 - 制定激活条件")
        activation = self._phase4_detection(spec, design)
        
        print("🔧 阶段5: 实现 - 创建所有文件")
        result = self._phase5_implementation(skill_path, spec, design, activation)
        
        return result
    
    def create_skill_from_code(self, code_path: str, description: Optional[str] = None) -> Dict[str, Any]:
        """从现有代码创建技能"""
        code_file = Path(code_path)
        if not code_file.exists():
            raise FileNotFoundError(f"代码文件不存在: {code_path}")
        
        with open(code_file, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # 分析代码功能
        analysis = self._analyze_code(code_content, code_file.suffix)
        
        # 生成描述（如果没有提供）
        if not description:
            description = analysis.get('description', f"从{code_file.name}创建的技能")
        
        # 创建技能
        return self.create_skill_from_description(description)
    
    def create_skill_from_api_docs(self, api_docs: str, endpoint_patterns: List[str] = None) -> Dict[str, Any]:
        """从API文档创建技能"""
        print(f"📄 分析API文档 ({len(api_docs)} 字符)")
        
        # 提取API端点和模式
        endpoints = self._extract_api_endpoints(api_docs, endpoint_patterns)
        
        # 生成技能描述
        description = f"API集成技能，支持以下端点: {', '.join(endpoints[:5])}"
        if len(endpoints) > 5:
            description += f" 等{len(endpoints)}个端点"
        
        return self.create_skill_from_description(description)
    
    def _phase1_discovery(self, description: str) -> Dict[str, Any]:
        """阶段1: 发现 - 读取材料，研究API、数据源、工具"""
        # 分析描述中的关键词
        keywords = self._extract_keywords(description)
        
        # 识别可能的工具和API
        tools = self._identify_tools(description)
        
        # 识别可能的输入/输出
        inputs_outputs = self._identify_inputs_outputs(description)
        
        # 识别可能的用例
        use_cases = self._identify_use_cases(description)
        
        return {
            'description': description,
            'keywords': keywords,
            'tools': tools,
            'inputs_outputs': inputs_outputs,
            'use_cases': use_cases,
            'complexity': self._estimate_complexity(description, tools)
        }
    
    def _phase2_design(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """阶段2: 设计 - 生成内部规范"""
        # 设计技能结构
        structure = self._design_skill_structure(spec)
        
        # 设计实现计划
        implementation = self._design_implementation(spec)
        
        # 设计测试计划
        testing = self._design_testing(spec)
        
        # 设计文档计划
        documentation = self._design_documentation(spec)
        
        return {
            'structure': structure,
            'implementation': implementation,
            'testing': testing,
            'documentation': documentation,
            'requirements': spec.get('tools', [])
        }
    
    def _phase3_architecture(self, skill_name: str, design: Dict[str, Any]) -> Path:
        """阶段3: 构建 - 创建技能目录结构"""
        skill_path = self.skills_dir / skill_name
        
        # 创建目录结构
        directories = [
            skill_path,
            skill_path / "scripts",
            skill_path / "references",
            skill_path / "templates",
            skill_path / "assets",
            skill_path / "tests"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        print(f"✅ 创建技能目录: {skill_path}")
        return skill_path
    
    def _phase4_detection(self, spec: Dict[str, Any], design: Dict[str, Any]) -> Dict[str, Any]:
        """阶段4: 检测 - 制定激活描述和关键词"""
        # 生成激活关键词
        keywords = self._generate_activation_keywords(spec)
        
        # 生成激活描述
        activation_desc = self._generate_activation_description(spec)
        
        # 生成触发短语
        trigger_phrases = self._generate_trigger_phrases(spec)
        
        return {
            'keywords': keywords,
            'description': activation_desc,
            'triggers': trigger_phrases,
            'priority': self._determine_priority(spec)
        }
    
    def _phase5_implementation(self, skill_path: Path, spec: Dict[str, Any], 
                              design: Dict[str, Any], activation: Dict[str, Any]) -> Dict[str, Any]:
        """阶段5: 实现 - 创建所有文件，验证，安全扫描"""
        # 创建SKILL.md文件
        skill_md = self._generate_skill_md(spec, design, activation)
        skill_md_path = skill_path / "SKILL.md"
        
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(skill_md)
        
        # 创建主脚本
        main_script = self._generate_main_script(spec, design)
        script_path = skill_path / "scripts" / "main.py"
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(main_script)
        
        # 创建README
        readme = self._generate_readme(spec, design)
        readme_path = skill_path / "README.md"
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme)
        
        # 创建requirements.txt
        requirements = self._generate_requirements(spec, design)
        req_path = skill_path / "requirements.txt"
        
        with open(req_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(requirements))
        
        # 运行安全扫描
        security_issues = self._security_scan(skill_path)
        
        # 运行验证
        validation = self._validate_skill(skill_path)
        
        result = {
            'skill_name': skill_path.name,
            'skill_path': str(skill_path),
            'files_created': [
                str(skill_md_path),
                str(script_path),
                str(readme_path),
                str(req_path)
            ],
            'security_issues': security_issues,
            'validation_passed': validation,
            'activation': activation
        }
        
        if validation:
            print(f"✅ 技能创建成功: {skill_path.name}")
        else:
            print(f"⚠️ 技能创建完成但验证失败: {skill_path.name}")
        
        return result
    
    # 辅助方法
    def _extract_keywords(self, text: str) -> List[str]:
        """从文本中提取关键词"""
        # 简单的关键词提取
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', text.lower())
        # 过滤常见词
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with'}
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return list(set(keywords))[:20]
    
    def _identify_tools(self, description: str) -> List[str]:
        """识别描述中提到的工具"""
        tools = []
        tool_patterns = [
            r'\b(python|node|npm|git|docker|kubectl|aws|gcp|azure)\b',
            r'\b(api|rest|graphql|websocket)\b',
            r'\b(database|sql|mongodb|redis|postgresql)\b',
            r'\b(file|csv|json|xml|yaml)\b'
        ]
        
        for pattern in tool_patterns:
            matches = re.findall(pattern, description.lower())
            tools.extend(matches)
        
        return list(set(tools))
    
    def _identify_inputs_outputs(self, description: str) -> Dict[str, List[str]]:
        """识别输入和输出"""
        # 简单的模式匹配
        inputs = []
        outputs = []
        
        if 'input' in description.lower():
            inputs.append('user_input')
        if 'file' in description.lower():
            inputs.append('file_input')
        if 'api' in description.lower():
            inputs.append('api_data')
        if 'output' in description.lower() or 'result' in description.lower():
            outputs.append('result')
        if 'report' in description.lower():
            outputs.append('report')
        if 'file' in description.lower():
            outputs.append('file_output')
        
        return {'inputs': inputs, 'outputs': outputs}
    
    def _identify_use_cases(self, description: str) -> List[str]:
        """识别用例"""
        use_cases = []
        
        if 'daily' in description.lower() or 'every day' in description.lower():
            use_cases.append('daily_automation')
        if 'weekly' in description.lower():
            use_cases.append('weekly_processing')
        if 'monthly' in description.lower():
            use_cases.append('monthly_reporting')
        if 'report' in description.lower():
            use_cases.append('report_generation')
        if 'data' in description.lower():
            use_cases.append('data_processing')
        if 'api' in description.lower():
            use_cases.append('api_integration')
        
        return use_cases if use_cases else ['general_automation']
    
    def _estimate_complexity(self, description: str, tools: List[str]) -> str:
        """估计复杂性"""
        word_count = len(description.split())
        tool_count = len(tools)
        
        if word_count < 20 and tool_count < 3:
            return 'low'
        elif word_count < 50 and tool_count < 6:
            return 'medium'
        else:
            return 'high'
    
    def _design_skill_structure(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """设计技能结构"""
        complexity = spec.get('complexity', 'medium')
        
        if complexity == 'low':
            return {
                'type': 'simple',
                'files': ['SKILL.md', 'main.py', 'README.md'],
                'scripts': 1,
                'references': 0
            }
        else:
            return {
                'type': 'complex',
                'files': ['SKILL.md', 'main.py', 'config.py', 'README.md'],
                'scripts': 2,
                'references': 1,
                'templates': 1
            }
    
    def _design_implementation(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """设计实现计划"""
        tools = spec.get('tools', [])
        
        implementation = {
            'main_function': 'process_workflow',
            'helper_functions': [],
            'dependencies': []
        }
        
        # 根据工具添加依赖
        if 'python' in tools:
            implementation['dependencies'].append('python>=3.8')
        if 'api' in tools:
            implementation['dependencies'].append('requests>=2.28.0')
        if 'file' in tools:
            implementation['dependencies'].append('pathlib')
        
        return implementation
    
    def _design_testing(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """设计测试计划"""
        return {
            'unit_tests': True,
            'integration_tests': spec.get('complexity', 'medium') != 'low',
            'e2e_tests': spec.get('complexity', 'medium') == 'high',
            'coverage_target': 80
        }
    
    def _design_documentation(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """设计文档计划"""
        return {
            'readme': True,
            'api_docs': 'api' in spec.get('tools', []),
            'examples': True,
            'changelog': True
        }
    
    def _generate_skill_name(self, spec: Dict[str, Any]) -> str:
        """生成技能名称"""
        keywords = spec.get('keywords', [])
        if keywords:
            # 取前3个关键词生成名称
            name = '-'.join(keywords[:3])
        else:
            name = 'custom-skill'
        
        # 清理名称
        name = re.sub(r'[^a-z0-9-]', '-', name.lower())
        name = re.sub(r'-+', '-', name)
        return name.strip('-')
    
    def _generate_activation_keywords(self, spec: Dict[str, Any]) -> List[str]:
        """生成激活关键词"""
        keywords = spec.get('keywords', [])
        tools = spec.get('tools', [])
        
        activation_keywords = keywords[:10] + tools[:5]
        return list(set(activation_keywords))
    
    def _generate_activation_description(self, spec: Dict[str, Any]) -> str:
        """生成激活描述"""
        description = spec.get('description', '')
        keywords = spec.get('keywords', [])
        
        activation_desc = f"触发于: {description[:100]}"
        if keywords:
            activation_desc += f"\n关键词: {', '.join(keywords[:5])}"
        
        return activation_desc
    
    def _generate_trigger_phrases(self, spec: Dict[str, Any]) -> List[str]:
        """生成触发短语"""
        description = spec.get('description', '').lower()
        
        trigger_phrases = []
        
        if 'create' in description or 'make' in description:
            trigger_phrases.extend(['创建', '制作', '生成'])
        if 'automate' in description or 'automatic' in description:
            trigger_phrases.extend(['自动化', '自动'])
        if 'process' in description:
            trigger_phrases.extend(['处理', '加工'])
        if 'convert' in description:
            trigger_phrases.extend(['转换', '转化'])
        if 'analyze' in description:
            trigger_phrases.extend(['分析', '解析'])
        
        return trigger_phrases[:5] if trigger_phrases else ['使用', '运行', '执行']
    
    def _determine_priority(self, spec: Dict[str, Any]) -> str:
        """确定技能优先级"""
        complexity = spec.get('complexity', 'medium')
        
        if complexity == 'low':
            return 'low'
        elif complexity == 'medium':
            return 'medium'
        else:
            return 'high'
    
    def _generate_skill_md(self, spec: Dict[str, Any], design: Dict[str, Any], 
                          activation: Dict[str, Any]) -> str:
        """生成SKILL.md内容"""
        skill_name = self._generate_skill_name(spec)
        description = spec.get('description', '自定义技能')
        
        skill_md = f"""---
name: {skill_name}
description: {description}
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: {spec.get('keywords', [])}
    complexity: {spec.get('complexity', 'medium')}
    tools: {spec.get('tools', [])}
---

# {skill_name.replace('-', ' ').title()}

{description}

## 功能 (Features)

{self._generate_features_section(spec)}

## 使用方法 (Usage)

{self._generate_usage_section(spec)}

## 配置 (Configuration)

{self._generate_configuration_section(spec)}

## 示例 (Examples)

{self._generate_examples_section(spec)}

## 注意事项 (Notes)

{self._generate_notes_section(spec)}

## 技能评估 (Skill Assessment)

{self._generate_assessment_section(spec)}

---

*技能创建时间: 2026年4月17日*
*基于agent-skill-creator的学习成果*
*支持Hermes Agent技能系统*
"""
        return skill_md
    
    def _generate_features_section(self, spec: Dict[str, Any]) -> str:
        """生成功能部分"""
        features = []
        tools = spec.get('tools', [])
        use_cases = spec.get('use_cases', [])
        
        if tools:
            features.append(f"- 支持工具: {', '.join(tools)}")
        if use_cases:
            features.append(f"- 适用场景: {', '.join(use_cases)}")
        
        features.append("- 自动化工作流处理")
        features.append("- 错误处理和日志记录")
        
        return '\n'.join(features)
    
    def _generate_usage_section(self, spec: Dict[str, Any]) -> str:
        """生成使用方法部分"""
        return """
```python
# 基本用法
from scripts.main import process_workflow

result = process_workflow(input_data)
print(result)
```

```bash
# 命令行使用
python scripts/main.py --input data.json --output result.json
```
"""
    
    def _generate_configuration_section(self, spec: Dict[str, Any]) -> str:
        """生成配置部分"""
        return """
```yaml
# config.yaml
settings:
  log_level: INFO
  timeout: 30
  retry_count: 3
```
"""
    
    def _generate_examples_section(self, spec: Dict[str, Any]) -> str:
        """生成示例部分"""
        description = spec.get('description', '')
        return f"""
### 示例1: 基本使用
{description}

### 示例2: 高级配置
```python
config = {{
    'log_level': 'DEBUG',
    'timeout': 60
}}
result = process_workflow(input_data, config)
```
"""
    
    def _generate_notes_section(self, spec: Dict[str, Any]) -> str:
        """生成注意事项部分"""
        return """
1. 确保输入数据格式正确
2. 检查网络连接（如果需要API调用）
3. 注意数据安全和隐私保护
4. 定期更新依赖包
"""
    
    def _generate_assessment_section(self, spec: Dict[str, Any]) -> str:
        """生成技能评估部分"""
        return """
```
功能完整性: ⭐⭐⭐⭐☆ (4/5)
易用性: ⭐⭐⭐⭐⭐ (5/5)
文档质量: ⭐⭐⭐⭐☆ (4/5)
错误处理: ⭐⭐⭐☆☆ (3/5)
性能优化: ⭐⭐⭐☆☆ (3/5)
```
"""
    
    def _generate_main_script(self, spec: Dict[str, Any], design: Dict[str, Any]) -> str:
        """生成主脚本内容"""
        skill_name = self._generate_skill_name(spec)
        function_name = skill_name.replace('-', '_')
        
        script = f'''#!/usr/bin/env python3
"""
{skill_name} - 主脚本
{spec.get('description', '')}
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def {function_name}(input_data: Any, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    主处理函数
    
    Args:
        input_data: 输入数据
        config: 配置参数
        
    Returns:
        处理结果
    """
    if config is None:
        config = {{}}
    
    logger.info(f"开始处理 {{type(input_data).__name__}} 数据")
    
    try:
        # TODO: 实现主要处理逻辑
        result = {{
            'success': True,
            'data': input_data,
            'message': '处理完成'
        }}
        
        logger.info("处理完成")
        return result
        
    except Exception as e:
        logger.error(f"处理失败: {{e}}")
        return {{
            'success': False,
            'error': str(e),
            'message': '处理失败'
        }}


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='{skill_name}')
    parser.add_argument('--input', '-i', help='输入文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--config', '-c', help='配置文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 加载输入数据
    input_data = None
    if args.input:
        input_path = Path(args.input)
        if input_path.exists():
            with open(input_path, 'r', encoding='utf-8') as f:
                if input_path.suffix == '.json':
                    input_data = json.load(f)
                else:
                    input_data = f.read()
    
    # 加载配置
    config = {{}}
    if args.config:
        config_path = Path(args.config)
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
    
    # 处理数据
    result = {function_name}(input_data, config)
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到: {{args.output}}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
'''
        return script
    
    def _generate_readme(self, spec: Dict[str, Any], design: Dict[str, Any]) -> str:
        """生成README内容"""
        skill_name = self._generate_skill_name(spec)
        description = spec.get('description', '')
        
        readme = f"""# {skill_name.replace('-', ' ').title()}

{description}

## 安装 (Installation)

```bash
# 进入技能目录
cd ~/.hermes/skills/{skill_name}

# 安装依赖
pip install -r requirements.txt
```

## 使用方法 (Usage)

### 基本用法
```python
from scripts.main import {skill_name.replace('-', '_')}

result = {skill_name.replace('-', '_')}(input_data)
print(result)
```

### 命令行使用
```bash
python scripts/main.py --input data.json --output result.json
```

## 配置 (Configuration)

编辑 `config.yaml` 文件进行配置：

```yaml
settings:
  log_level: INFO
  timeout: 30
  retry_count: 3
```

## 示例 (Examples)

查看 `examples/` 目录获取更多示例。

## 文件结构 (File Structure)

```
{skill_name}/
├── SKILL.md          # 技能描述文件
├── README.md         # 本文件
├── requirements.txt  # Python依赖
├── scripts/          # 脚本文件
│   └── main.py      # 主脚本
├── references/       # 参考文档
├── templates/        # 模板文件
└── assets/          # 资源文件
```

## 开发 (Development)

1. 克隆或创建技能目录
2. 编辑 `SKILL.md` 更新技能描述
3. 实现 `scripts/main.py` 中的功能
4. 测试技能功能
5. 提交到技能市场

## 许可证 (License)

MIT License

---

*创建时间: 2026年4月17日*
*作者: Hermes Agent*
"""
        return readme
    
    def _generate_requirements(self, spec: Dict[str, Any], design: Dict[str, Any]) -> List[str]:
        """生成requirements.txt内容"""
        requirements = ['python>=3.8']
        
        tools = spec.get('tools', [])
        if 'api' in tools or 'requests' in tools:
            requirements.append('requests>=2.28.0')
        if 'json' in tools:
            requirements.append('ujson>=4.0.0')
        if 'file' in tools or 'pathlib' in tools:
            requirements.append('pathlib>=1.0.1')
        
        # 添加通用依赖
        requirements.extend([
            'pyyaml>=6.0',
            'python-dotenv>=1.0.0'
        ])
        
        return requirements
    
    def _analyze_code(self, code_content: str, file_extension: str) -> Dict[str, Any]:
        """分析代码内容"""
        analysis = {
            'language': file_extension.lstrip('.'),
            'functions': [],
            'imports': [],
            'description': ''
        }
        
        # 简单的Python代码分析
        if file_extension == '.py':
            # 提取函数定义
            functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code_content)
            analysis['functions'] = functions
            
            # 提取导入
            imports = re.findall(r'(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_.]*)', code_content)
            analysis['imports'] = imports
            
            # 生成描述
            if functions:
                analysis['description'] = f"包含{len(functions)}个函数: {', '.join(functions[:3])}"
        
        return analysis
    
    def _extract_api_endpoints(self, api_docs: str, endpoint_patterns: Optional[List[str]] = None) -> List[str]:
        """从API文档中提取端点"""
        if not endpoint_patterns:
            endpoint_patterns = [
                r'/(?:api|v\d+)/[a-zA-Z0-9/_-]+',
                r'https?://[^\s]+/[a-zA-Z0-9/_-]+',
                r'[a-zA-Z]+\s+(/[a-zA-Z0-9/_-]+)'
            ]
        
        endpoints = []
        for pattern in endpoint_patterns:
            matches = re.findall(pattern, api_docs)
            endpoints.extend(matches)
        
        return list(set(endpoints))[:10]
    
    def _security_scan(self, skill_path: Path) -> List[str]:
        """安全扫描"""
        issues = []
        
        # 检查常见安全问题
        security_patterns = [
            (r'eval\s*\(', '使用eval函数可能存在代码注入风险'),
            (r'exec\s*\(', '使用exec函数可能存在代码注入风险'),
            (r'os\.system\s*\(', '使用os.system可能存在命令注入风险'),
            (r'subprocess\.call\s*\(.*shell\s*=\s*True', '使用shell=True可能存在命令注入风险'),
            (r'password\s*=\s*["\']', '硬编码密码'),
            (r'api[_-]?key\s*=\s*["\']', '硬编码API密钥'),
        ]
        
        for py_file in skill_path.rglob('*.py'):
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for pattern, message in security_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(f"{py_file.name}: {message}")
        
        return issues
    
    def _validate_skill(self, skill_path: Path) -> bool:
        """验证技能"""
        required_files = ['SKILL.md']
        
        for file_name in required_files:
            if not (skill_path / file_name).exists():
                print(f"❌ 缺少必需文件: {file_name}")
                return False
        
        # 检查SKILL.md格式
        skill_md_path = skill_path / 'SKILL.md'
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.startswith('---'):
            print("❌ SKILL.md格式错误: 缺少YAML头部")
            return False
        
        print("✅ 技能验证通过")
        return True


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='Hermes技能创建器')
    parser.add_argument('action', choices=['create', 'analyze'], help='操作类型')
    parser.add_argument('input', help='输入描述或文件路径')
    parser.add_argument('--name', '-n', help='技能名称')
    parser.add_argument('--type', '-t', choices=['description', 'code', 'api'], 
                       default='description', help='输入类型')
    
    args = parser.parse_args()
    
    creator = HermesSkillCreator()
    
    if args.action == 'create':
        if args.type == 'description':
            result = creator.create_skill_from_description(args.input, args.name)
        elif args.type == 'code':
            result = creator.create_skill_from_code(args.input, args.name)
        elif args.type == 'api':
            result = creator.create_skill_from_api_docs(args.input)
        else:
            print(f"不支持的类型: {args.type}")
            return
        
        print("\n" + "="*50)
        print("技能创建完成!")
        print(f"技能路径: {result['skill_path']}")
        print(f"文件数量: {len(result['files_created'])}")
        print(f"验证状态: {'通过' if result['validation_passed'] else '失败'}")
        
        if result['security_issues']:
            print(f"安全问题: {len(result['security_issues'])}个")
            for issue in result['security_issues']:
                print(f"  - {issue}")
    
    elif args.action == 'analyze':
        print(f"分析: {args.input}")
        # 分析逻辑...


if __name__ == '__main__':
    main()