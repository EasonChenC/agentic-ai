"""
Example: follow up on unread emails from boss and mark them as read.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import aisuite as ai

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import email_tools
from display_functions import pretty_print_chat_completion


def _apply_proxy_settings() -> None:
    http_proxy = os.getenv("HTTP_PROXY")
    https_proxy = os.getenv("HTTPS_PROXY")

    if http_proxy:
        os.environ["HTTP_PROXY"] = http_proxy
        os.environ["http_proxy"] = http_proxy
    if https_proxy:
        os.environ["HTTPS_PROXY"] = https_proxy
        os.environ["https_proxy"] = https_proxy


def build_prompt(user_request: str) -> str:
    return (
        "You are an email assistant. Use tools to read, search, and manage emails. "
        "Ask for missing details when needed. Keep responses concise.\n\n"
        f"User request: {user_request}"
    )


def test_followup_boss():
    """测试：跟进老板的未读邮件"""
    load_dotenv()
    _apply_proxy_settings()

    client = ai.Client()
    prompt_ = build_prompt(
        "检查来自 alice@work.com 的未读邮件，将其标记为已读，并发送一封礼貌的跟进邮件。"
    )

    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{"role": "user", "content": prompt_}],
        tools=[
            email_tools.search_unread_from_sender,
            email_tools.list_unread_emails,
            email_tools.search_emails,
            email_tools.get_email,
            email_tools.mark_email_as_read,
            email_tools.send_email,
        ],
        max_turns=5,
    )

    pretty_print_chat_completion(response)
    print(response.choices[0].message.content)


def test_list_unread_by_sender():
    """测试：查询所有未读邮件并按发件人整理"""
    load_dotenv()
    _apply_proxy_settings()

    client = ai.Client()
    prompt_ = build_prompt(
        "请执行以下任务：\n"
        "1. 使用 list_unread_emails 工具获取所有未读邮件\n"
        "2. 分析返回的邮件数据，按发件人（sender）分组\n"
        "3. 对每个发件人，统计未读邮件数量并列出邮件主题\n"
        "4. 用清晰的格式展示结果，例如：\n"
        "   发件人：xxx@email.com\n"
        "   - 未读邮件数量：N\n"
        "   - 邮件主题：主题1, 主题2\n\n"
        "请直接执行这个任务，不要询问是否需要执行。"
    )

    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{"role": "user", "content": prompt_}],
        tools=[
            email_tools.list_unread_emails,
            email_tools.get_email,
        ],
        max_turns=5,
    )

    pretty_print_chat_completion(response)
    print("\n" + "="*60)
    print("未读邮件整理结果：")
    print("="*60)
    print(response.choices[0].message.content)


def main():
    """主函数：运行测试"""
    print("选择要运行的测试：")
    print("1. 跟进老板的未读邮件")
    print("2. 查询所有未读邮件并按发件人整理")
    print("3. 运行所有测试")

    choice = input("\n请输入选项 (1/2/3，默认为2): ").strip() or "2"

    if choice == "1":
        print("\n运行测试1：跟进老板的未读邮件\n")
        test_followup_boss()
    elif choice == "2":
        print("\n运行测试2：查询所有未读邮件并按发件人整理\n")
        test_list_unread_by_sender()
    elif choice == "3":
        print("\n运行所有测试\n")
        print("\n" + "="*60)
        print("测试1：跟进老板的未读邮件")
        print("="*60 + "\n")
        test_followup_boss()

        print("\n\n" + "="*60)
        print("测试2：查询所有未读邮件并按发件人整理")
        print("="*60 + "\n")
        test_list_unread_by_sender()
    else:
        print("无效的选项，运行默认测试2")
        test_list_unread_by_sender()


if __name__ == "__main__":
    main()
