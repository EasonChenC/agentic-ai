"""
Multi-Tool Orchestration Example - Advanced Tool Coordination

This script demonstrates:
1. LLM orchestrating multiple tools in sequence
2. Intelligent tool selection for complex tasks
3. Information flow between different tools
4. Real-world multi-step workflows

多工具协同示例 - 高级工具编排
演示LLM如何智能地协调多个工具完成复杂任务
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import aisuite as ai
from agent_tools import ALL_TOOLS
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


def example_1_weather_and_file():
    """
    Example 1: Get weather and save to file
    示例 1: 获取天气并保存到文件

    This demonstrates:
    - Sequential tool usage (weather → file)
    - Information passing between tools
    """
    print("=" * 60)
    print("Example 1: Weather Report + File Writing")
    print("示例 1: 天气报告 + 文件写入")
    print("=" * 60)

    client = ai.Client()

    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{
            "role": "user",
            "content": "请帮我查询当前天气，然后创建一个名为 weather_report.txt 的文件，把天气信息写进去"
        }],
        tools=ALL_TOOLS,
        max_turns=10
    )

    pretty_print_chat_completion(response)

    # Verify the file was created
    weather_file = Path(__file__).parent.parent / "weather_report.txt"
    if weather_file.exists():
        print("\n✅ 文件已创建！内容如下：")
        print("─" * 60)
        print(weather_file.read_text(encoding='utf-8'))
        print("─" * 60)


def example_2_qrcode_and_reminder():
    """
    Example 2: Generate QR code and create reminder
    示例 2: 生成二维码并创建提醒

    This demonstrates:
    - Parallel task handling
    - Multiple independent tools
    """
    print("\n" + "=" * 60)
    print("Example 2: QR Code + Reminder File")
    print("示例 2: 二维码 + 提醒文件")
    print("=" * 60)

    client = ai.Client()

    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{
            "role": "user",
            "content": """请帮我完成两件事：
1. 生成一个跳转到 https://github.com 的二维码，文件名为 github_qr
2. 创建一个 reminder.txt 文件，提醒我明天下午3点查看GitHub"""
        }],
        tools=ALL_TOOLS,
        max_turns=10
    )

    pretty_print_chat_completion(response)

    # Check results
    qr_file = Path(__file__).parent.parent / "output" / "github_qr.png"
    reminder_file = Path(__file__).parent.parent / "reminder.txt"

    print("\n📊 执行结果：")
    if qr_file.exists():
        print(f"✅ 二维码已生成: {qr_file}")
    else:
        print("❌ 二维码未找到")

    if reminder_file.exists():
        print(f"✅ 提醒文件已创建: {reminder_file}")
        print(f"   内容: {reminder_file.read_text(encoding='utf-8')}")
    else:
        print("❌ 提醒文件未找到")


def example_3_complex_workflow():
    """
    Example 3: Complex multi-tool workflow
    示例 3: 复杂的多工具工作流

    This demonstrates:
    - 3+ tools in sequence
    - Complex information flow
    - Real-world scenario
    """
    print("\n" + "=" * 60)
    print("Example 3: Complex Multi-Tool Workflow")
    print("示例 3: 复杂多工具工作流")
    print("=" * 60)

    client = ai.Client()

    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{
            "role": "user",
            "content": """请帮我完成以下任务：
1. 查询当前时间和天气
2. 创建一个 daily_report.txt 文件，包含时间和天气信息
3. 生成一个包含文本 "Daily Report Created" 的二维码，文件名为 report_qr"""
        }],
        tools=ALL_TOOLS,
        max_turns=15
    )

    pretty_print_chat_completion(response)

    # Verify all outputs
    print("\n📊 任务完成情况：")

    report_file = Path(__file__).parent.parent / "daily_report.txt"
    if report_file.exists():
        print("✅ 日报文件已创建")
        print("─" * 60)
        print(report_file.read_text(encoding='utf-8'))
        print("─" * 60)

    qr_file = Path(__file__).parent.parent / "output" / "report_qr.png"
    if qr_file.exists():
        print(f"✅ 二维码已生成: {qr_file}")


def example_4_conditional_logic():
    """
    Example 4: Conditional tool usage based on context
    示例 4: 基于上下文的条件工具使用

    This demonstrates:
    - LLM making decisions about which tools to use
    - Context-aware tool selection
    """
    print("\n" + "=" * 60)
    print("Example 4: Context-Aware Tool Selection")
    print("示例 4: 上下文感知的工具选择")
    print("=" * 60)

    client = ai.Client()

    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{
            "role": "user",
            "content": """请帮我创建一个天气备忘录：
- 如果当前温度高于70°F，提醒我带防晒霜
- 如果低于70°F，提醒我带外套
- 将这个提醒保存到 weather_advice.txt 文件"""
        }],
        tools=ALL_TOOLS,
        max_turns=10
    )

    pretty_print_chat_completion(response)

    advice_file = Path(__file__).parent.parent / "weather_advice.txt"
    if advice_file.exists():
        print("\n✅ 天气建议已保存：")
        print("─" * 60)
        print(advice_file.read_text(encoding='utf-8'))
        print("─" * 60)


def main():
    """Run all multi-tool orchestration examples"""
    print("\n🚀 Multi-Tool Orchestration Examples")
    print("多工具协同编排示例")
    print("=" * 60)

    try:
        # Example 1: Weather + File (2 tools)
        # example_1_weather_and_file()

        # Example 2: QR Code + Reminder (2 tools, parallel)
        # example_2_qrcode_and_reminder()

        # Example 3: Time + Weather + File + QR Code (4 tools)
        # example_3_complex_workflow()

        # Example 4: Conditional logic with tools
        example_4_conditional_logic()

        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("✅ 所有示例运行成功！")
        print("=" * 60)

        print("\n💡 Key Takeaways / 关键要点:")
        print("1. LLM can orchestrate multiple tools in sequence")
        print("   LLM可以按顺序编排多个工具")
        print("2. Information flows naturally between tools")
        print("   信息在工具之间自然流动")
        print("3. LLM makes intelligent decisions about tool order")
        print("   LLM智能决定工具调用顺序")
        print("4. Complex workflows can be expressed in natural language")
        print("   复杂工作流可以用自然语言表达")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please ensure:")
        print("1. Dependencies are installed: pip install -r requirements.txt")
        print("2. .env file is configured with API keys")
        print("3. Proxy settings are correct (if needed)")


if __name__ == "__main__":
    main()
