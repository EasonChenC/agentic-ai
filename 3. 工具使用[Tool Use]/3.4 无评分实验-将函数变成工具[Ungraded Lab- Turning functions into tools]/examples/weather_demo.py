"""
Weather Tool Demonstration

Shows how the LLM can:
1. Automatically detect user location via IP
2. Fetch real-time weather data
3. Present information in natural language

天气工具演示
展示LLM如何自动检测位置、获取实时天气数据并以自然语言呈现
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import aisuite as ai
from agent_tools import get_weather_from_ip
from display_functions import pretty_print_chat_completion


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


def main():
    print("=" * 60)
    print("Weather Information Demo")
    print("天气信息演示")
    print("=" * 60)

    client = ai.Client()

    # Test the tool directly first
    print("\n1. Direct tool call (直接调用工具):")
    print(get_weather_from_ip())

    # Now use it through the LLM
    print("\n2. LLM-mediated tool call (通过LLM调用工具):")

    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{
            "role": "user",
            "content": "今天天气怎么样？需要带伞吗？"
        }],
        tools=[get_weather_from_ip],
        max_turns=5
    )

    pretty_print_chat_completion(response)

    print("\n💡 Note: Weather data is based on your IP location")
    print("   The LLM interprets the raw temperature data and")
    print("   provides contextual advice!")
    print("\n💡 注意：天气数据基于您的IP位置")
    print("   LLM会解释原始温度数据并提供上下文建议！")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please ensure your .env file is configured correctly.")
