"""
Basic Usage Example - Getting Started with AI Agent Tools

This script demonstrates:
1. Setting up the AISuite client
2. Providing tools to the LLM
3. Making a simple tool call
4. Understanding the response structure

基础使用示例 - AI智能体工具入门
演示如何设置客户端、提供工具给LLM、进行简单的工具调用
"""

import os
from dotenv import load_dotenv

import aisuite as ai
from agent_tools import get_current_time, ALL_TOOLS
from display_functions import pretty_print_chat_completion


# 加载环境变量
load_dotenv()

# 设置代理（如果环境变量中有配置）
http_proxy = os.getenv("HTTP_PROXY")
https_proxy = os.getenv("HTTPS_PROXY")

if http_proxy:
    os.environ["HTTP_PROXY"] = http_proxy
    os.environ["http_proxy"] = http_proxy
if https_proxy:
    os.environ["HTTPS_PROXY"] = https_proxy
    os.environ["https_proxy"] = https_proxy

print(f"🌐 代理配置: HTTP_PROXY={http_proxy}, HTTPS_PROXY={https_proxy}")


def basic_time_example():
    """Demonstrates basic tool usage with get_current_time"""
    print("=" * 60)
    print("Example 1: Basic Time Query")
    print("示例 1: 基础时间查询")
    print("=" * 60)

    # Initialize AISuite client
    client = ai.Client()

    # Create user message
    messages = [{
        "role": "user",
        "content": "现在几点？"
    }]

    # Call LLM with tool access
    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=messages,
        tools=[get_current_time],  # Provide single tool
        max_turns=5
    )

    # Display formatted response
    pretty_print_chat_completion(response)

    # Extract final answer
    print("\n📝 Final Answer:")
    print(response.choices[0].message.content)


def multi_tool_example():
    """Demonstrates LLM choosing from multiple tools"""
    print("\n" + "=" * 60)
    print("Example 2: Multi-Tool Selection")
    print("示例 2: 多工具选择")
    print("=" * 60)

    client = ai.Client()

    # Ask a question that requires tool selection
    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{
            "role": "user",
            "content": "请告诉我现在的时间"
        }],
        tools=ALL_TOOLS,  # Provide all available tools
        max_turns=10
    )

    pretty_print_chat_completion(response)


if __name__ == "__main__":
    print("\n🚀 AI Agent Tools - Basic Usage Examples")
    print("AI 智能体工具 - 基础使用示例\n")

    try:
        basic_time_example()
        multi_tool_example()

        print("\n✅ Examples completed successfully!")
        print("✅ 示例运行成功！")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please make sure you have:")
        print("1. Installed dependencies: pip install -r requirements.txt")
        print("2. Set up .env file with your OPENAI_API_KEY")
