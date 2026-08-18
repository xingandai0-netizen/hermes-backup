---
name: langchain-agent-fundamentals
description: LangChain Agent开发基础，支持构建智能AI代理系统
version: 1.0.0
author: Hermes Agent
---

# LangChain Agent基础

## 核心组件

### 模型调用
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4", temperature=0)
response = llm.invoke("你好")

### 提示模板
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}助手"),
    ("human", "{input}")
])

### 记忆系统
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
memory.save_context({"input": "你好"}, {"output": "你好！"})

### 工具集成
from langchain_core.tools import tool
@tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    return str(eval(expression))

### Agent架构
from langchain.agents import AgentExecutor, create_openai_tools_agent
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

## Agent类型

| 类型 | 描述 | 适用场景 |
|------|------|---------|
| ReAct | 推理+行动 | 复杂决策 |
| Plan-and-Execute | 规划+执行 | 多步骤任务 |
| Conversational | 对话式 | 聊天机器人 |
| Tool-using | 工具调用 | 任务自动化 |

## 安装
```bash
pip install langchain langchain-openai langchain-community
```
