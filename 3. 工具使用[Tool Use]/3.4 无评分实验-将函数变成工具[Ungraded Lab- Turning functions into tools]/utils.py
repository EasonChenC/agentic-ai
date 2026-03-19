"""
Utility functions for the AI Agent Tools Lab.
Provides helpers for testing, debugging, and displaying results.

工具辅助函数模块
提供测试、调试和结果显示的辅助功能
"""

import json
from typing import Any, Dict, List


def validate_api_response(response: Dict[str, Any]) -> bool:
    """
    Validates that an API response has the expected structure.

    验证API响应是否具有预期的结构。

    Args:
        response: Dictionary response from LLM API

    Returns:
        bool: True if response is valid
    """
    required_keys = ["choices"]
    return all(key in response for key in required_keys)


def extract_tool_calls(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extracts tool call information from LLM response.

    从LLM响应中提取工具调用信息。

    Args:
        response: Chat completion response from AISuite

    Returns:
        List of tool call dictionaries
    """
    tool_calls = []

    try:
        choice = response.get("choices", [{}])[0]
        intermediate = choice.get("intermediate_messages", [])

        for step in intermediate:
            if hasattr(step, "tool_calls") and step.tool_calls:
                for call in step.tool_calls:
                    tool_calls.append({
                        "name": call.function.name,
                        "arguments": json.loads(call.function.arguments)
                    })
    except Exception as e:
        print(f"Error extracting tool calls: {e}")

    return tool_calls


def format_tool_sequence(tool_calls: List[Dict[str, Any]]) -> str:
    """
    Creates a visual representation of tool call sequence.

    创建工具调用序列的可视化表示。

    Args:
        tool_calls: List of tool call dictionaries

    Returns:
        Formatted string showing tool sequence
    """
    if not tool_calls:
        return "No tools called"

    names = [call["name"] for call in tool_calls]
    return " → ".join(names)


def create_message_prompt(user_prompt: str, system_prompt: str = None) -> List[Dict[str, str]]:
    """
    Creates properly formatted message list for LLM.

    为LLM创建格式正确的消息列表。

    Args:
        user_prompt: The user's instruction
        system_prompt: Optional system-level instructions

    Returns:
        List of message dictionaries
    """
    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    messages.append({
        "role": "user",
        "content": user_prompt
    })

    return messages


def save_json(data: Any, filepath: str, indent: int = 2) -> None:
    """
    Saves data to JSON file with pretty formatting.

    将数据保存到JSON文件，使用美观的格式。

    Args:
        data: Data to save (dict, list, etc.)
        filepath: Destination file path
        indent: JSON indentation level
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    print(f"✅ Saved to: {filepath}")


def load_json(filepath: str) -> Any:
    """
    Loads data from JSON file.

    从JSON文件加载数据。

    Args:
        filepath: Source file path

    Returns:
        Parsed JSON data
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def print_section(title: str, width: int = 60):
    """
    Prints a formatted section header.

    打印格式化的章节标题。

    Args:
        title: Section title
        width: Width of the separator line
    """
    print("\n" + "=" * width)
    print(title)
    print("=" * width)


def print_tool_info(tool_func):
    """
    Prints information about a tool function.

    打印工具函数的信息。

    Args:
        tool_func: Function object
    """
    print(f"\n📌 Tool: {tool_func.__name__}")
    if tool_func.__doc__:
        # Get first line of docstring
        first_line = tool_func.__doc__.strip().split('\n')[0]
        print(f"   Description: {first_line}")
