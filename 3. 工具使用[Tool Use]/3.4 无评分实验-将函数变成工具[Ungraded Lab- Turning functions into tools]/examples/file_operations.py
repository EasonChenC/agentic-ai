"""
File Writing Tool Demonstration

Shows how LLM can:
1. Create text files based on natural language instructions
2. Infer appropriate filenames
3. Format content appropriately

文件写入工具演示
展示LLM如何基于自然语言指令创建文件、推断文件名并格式化内容
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import aisuite as ai
from agent_tools import write_txt_file
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
    print("File Operations Demo")
    print("文件操作演示")
    print("=" * 60)

    client = ai.Client()

    # Example 1: Simple reminder
    print("\nExample 1: Creating a reminder file")
    print("示例 1: 创建备忘录文件")
    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{
            "role": "user",
            "content": "请帮我创建一个备忘录 reminders.txt，提醒我明天下午3点开会"
        }],
        tools=[write_txt_file],
        max_turns=5
    )

    pretty_print_chat_completion(response)

    # Verify file was created
    reminder_file = Path(__file__).parent.parent / "reminders.txt"
    if reminder_file.exists():
        print("\n📄 File contents:")
        print(reminder_file.read_text(encoding='utf-8'))

    # Example 2: More complex content
    print("\n" + "=" * 60)
    print("Example 2: Creating a todo list")
    print("示例 2: 创建待办事项列表")
    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{
            "role": "user",
            "content": """创建一个 todo.txt 文件，列出今天要做的3件事：
1. 学习 AI Agent 工具
2. 完成代码实验
3. 写项目文档"""
        }],
        tools=[write_txt_file],
        max_turns=5
    )

    pretty_print_chat_completion(response)

    todo_file = Path(__file__).parent.parent / "todo.txt"
    if todo_file.exists():
        print("\n📄 File contents:")
        print(todo_file.read_text(encoding='utf-8'))


if __name__ == "__main__":
    try:
        main()
        print("\n✅ File operations completed!")
        print("✅ 文件操作完成！")
    except Exception as e:
        print(f"\n❌ Error: {e}")
