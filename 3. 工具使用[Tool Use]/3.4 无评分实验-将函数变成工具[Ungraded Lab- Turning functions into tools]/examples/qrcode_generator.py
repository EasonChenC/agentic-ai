"""
QR Code Generation Demonstration

Shows how to:
1. Generate basic QR codes
2. Embed logos in QR codes
3. Handle different data types (URLs, text)

二维码生成演示
展示如何生成基础二维码、嵌入Logo和处理不同数据类型
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import aisuite as ai
from agent_tools import generate_qr_code
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
    print("QR Code Generation Demo")
    print("二维码生成演示")
    print("=" * 60)

    client = ai.Client()

    # Example 1: Simple QR code without logo
    print("\nExample 1: Basic QR code")
    print("示例 1: 基础二维码")
    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{
            "role": "user",
            "content": "生成一个包含文本 'Hello, AI Agent!' 的二维码，文件名为 hello_qr"
        }],
        tools=[generate_qr_code],
        max_turns=5
    )

    pretty_print_chat_completion(response)

    # Example 2: QR code with URL
    print("\n" + "=" * 60)
    print("Example 2: QR code for website")
    print("示例 2: 网站二维码")

    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{
            "role": "user",
            "content": "生成一个跳转到 www.deeplearning.ai 的二维码，文件名为 dl_qr_code"
        }],
        tools=[generate_qr_code],
        max_turns=5
    )

    pretty_print_chat_completion(response)

    # Check if QR code was generated
    output_dir = Path(__file__).parent.parent / "output"
    qr_files = list(output_dir.glob("*.png"))

    if qr_files:
        print(f"\n✅ Generated {len(qr_files)} QR code(s):")
        for qr_file in qr_files:
            print(f"   - {qr_file.name}")
    else:
        print("\n⚠️  No QR codes found in output directory")

    # Note about logo embedding
    logo_path = Path(__file__).parent.parent / "assets" / "dl_logo.jpg"
    if not logo_path.exists():
        print("\n💡 Tip: To generate QR codes with logos:")
        print("   1. Add a logo image to assets/dl_logo.jpg")
        print("   2. The generate_qr_code function will automatically embed it")
        print("\n💡 提示：要生成带Logo的二维码：")
        print("   1. 将Logo图片添加到 assets/dl_logo.jpg")
        print("   2. generate_qr_code 函数会自动嵌入Logo")


if __name__ == "__main__":
    try:
        main()
        print("\n✅ QR code generation completed!")
        print("✅ 二维码生成完成！")
    except Exception as e:
        print(f"\n❌ Error: {e}")
