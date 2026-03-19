# AI Agent Tools Lab - 将函数变成工具

## 📖 项目简介 / Project Overview

这是一个展示如何使用 AISuite 将 Python 函数转换为 LLM 工具的实验项目。通过本项目，你将学习如何让大语言模型（LLM）调用实际的 Python 函数来完成各种任务。

This lab demonstrates how to transform Python functions into LLM tools using AISuite. You'll learn how to enable Large Language Models to call real Python functions to accomplish various tasks.

### 🎯 学习目标 / Learning Objectives

- 理解工具调用（Tool Calling）的设计模式
- 掌握如何将 Python 函数暴露给 LLM
- 学习管理参数传递与执行流程
- 验证多步工具编排的输出

---

## 🛠️ 工具列表 / Available Tools

本项目提供 4 个工具函数：

### 1. **get_current_time**
获取当前时间
- 参数：无
- 返回：当前时间字符串 (HH:MM:SS)

### 2. **get_weather_from_ip**
基于 IP 地址获取天气信息
- 参数：无（自动检测位置）
- 返回：当前温度、最高温、最低温

### 3. **write_txt_file**
写入文本文件
- 参数：
  - `file_path` (str): 文件路径
  - `content` (str): 文件内容
- 返回：成功消息

### 4. **generate_qr_code**
生成二维码图片
- 参数：
  - `data` (str): 要编码的数据
  - `filename` (str): 输出文件名
  - `image_path` (str, optional): Logo 图片路径
- 返回：成功消息

---

## 🚀 快速开始 / Quick Start

### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 配置环境 / Configure Environment

复制环境变量模板并填入你的 API 密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件，添加你的 OpenAI API 密钥：

```
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. 运行示例 / Run Examples

```bash
# 基础使用示例
python examples/basic_usage.py

# 天气工具演示
python examples/weather_demo.py

# 文件操作演示
python examples/file_operations.py

# 二维码生成演示
python examples/qrcode_generator.py
```

---

## 📁 项目结构 / Project Structure

```
3.4 无评分实验-将函数变成工具/
│
├── README.md                 # 项目说明
├── requirements.txt          # Python 依赖
├── .env.example             # 环境变量模板
├── .gitignore               # Git 忽略规则
│
├── config.py                # 配置管理
├── agent_tools.py           # 4个工具函数
├── display_functions.py     # 显示辅助函数
├── utils.py                 # 通用工具
│
├── examples/                # 示例脚本
│   ├── basic_usage.py
│   ├── weather_demo.py
│   ├── file_operations.py
│   └── qrcode_generator.py
│
├── assets/                  # 资源文件
│   └── (place logo files here)
│
├── output/                  # 生成文件输出目录
│
└── *.ipynb                  # 原始 Jupyter 笔记本
```

---

## 💻 使用方法 / Usage

### 基础示例 / Basic Example

```python
import aisuite as ai
from agent_tools import get_current_time

# 初始化客户端
client = ai.Client()

# 调用 LLM 并提供工具
response = client.chat.completions.create(
    model="openai:gpt-4o",
    messages=[{"role": "user", "content": "现在几点？"}],
    tools=[get_current_time],
    max_turns=5
)

print(response.choices[0].message.content)
```

### 多工具编排 / Multi-Tool Orchestration

```python
from agent_tools import ALL_TOOLS

response = client.chat.completions.create(
    model="openai:gpt-4o",
    messages=[{
        "role": "user",
        "content": "请帮我生成一个二维码，并创建一个包含当前天气的备忘录"
    }],
    tools=ALL_TOOLS,  # 提供所有工具
    max_turns=10
)
```

---

## 🔧 配置说明 / Configuration

### 环境变量 / Environment Variables

| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | ✅ | - |
| `TEMPERATURE_UNIT` | 温度单位 | ❌ | fahrenheit |
| `DEFAULT_TIMEZONE` | 时区设置 | ❌ | auto |
| `LOG_LEVEL` | 日志级别 | ❌ | INFO |

### 支持的模型 / Supported Models

- `openai:gpt-4o` - 推荐用于复杂任务
- `openai:gpt-4o-mini` - 快速且经济
- `openai:gpt-3.5-turbo` - 简单任务

---

## 📚 关键概念 / Key Concepts

### 工具调用流程 / Tool Calling Flow

1. **用户提示** → LLM 接收指令
2. **工具选择** → LLM 决定使用哪个工具
3. **参数推断** → LLM 从用户消息中提取参数
4. **本地执行** → 在你的机器上运行工具函数
5. **结果返回** → 工具输出返回给 LLM
6. **最终响应** → LLM 基于工具结果生成回复

### 自动 vs 手动模式 / Automatic vs Manual Mode

**自动模式**（推荐）：
```python
response = client.chat.completions.create(
    tools=[function],
    max_turns=5  # AISuite 自动处理工具调用
)
```

**手动模式**：
```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "...",
        "parameters": {}
    }
}]

response = client.chat.completions.create(tools=tools)
# 需要手动处理 tool_calls
```

---

## 🆘 常见问题 / FAQ

### Q: 为什么 get_weather_from_ip 返回错误？
A: 确保你的网络可以访问 ipinfo.io 和 open-meteo.com API。

### Q: 二维码中的 Logo 显示不正常？
A: 确保 Logo 图片：
- 存在于 `assets/dl_logo.jpg`
- 文件格式正确（JPG/PNG）
- 尺寸适中（建议 < 500KB）

### Q: OPENAI_API_KEY 错误？
A: 检查：
1. `.env` 文件是否存在
2. API 密钥是否有效
3. 是否有足够的配额

### Q: Windows 下路径问题？
A: 本项目使用 `pathlib` 处理路径，完全兼容 Windows。所有路径会自动转换。

---

## 🎓 课程信息 / Course Information

**课程来源**: DeepLearning.AI - Agentic AI
**模块**: M3 工具使用 (Tool Use)
**实验**: 3.4 将函数变成工具

---

## 📝 许可 / License

本项目仅用于学习目的。

---

## ✨ 总结 / Summary

完成本项目后，你将掌握：
- ✅ 完整的项目结构和配置管理
- ✅ 模块化、可复用的工具函数
- ✅ LLM 工具调用的核心机制
- ✅ 多工具协同编排的能力
- ✅ 跨平台兼容的代码实现

这是一个专业、完整、易于使用的 AI Agent 工具项目！

Happy Coding! 祝编码愉快！ 🚀
