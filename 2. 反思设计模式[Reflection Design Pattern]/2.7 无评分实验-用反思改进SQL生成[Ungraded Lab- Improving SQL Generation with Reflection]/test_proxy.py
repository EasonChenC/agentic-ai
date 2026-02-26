"""
测试代理配置和 Google Vertex AI 连接
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置代理
http_proxy = os.getenv("HTTP_PROXY")
https_proxy = os.getenv("HTTPS_PROXY")

if http_proxy:
    os.environ["HTTP_PROXY"] = http_proxy
    os.environ["http_proxy"] = http_proxy
if https_proxy:
    os.environ["HTTPS_PROXY"] = https_proxy
    os.environ["https_proxy"] = https_proxy

print("="*70)
print("🧪 测试代理和 Vertex AI 连接")
print("="*70)
print(f"\n🌐 代理配置:")
print(f"  - HTTP_PROXY: {http_proxy}")
print(f"  - HTTPS_PROXY: {https_proxy}")

print(f"\n🔑 Vertex AI 配置:")
print(f"  - GOOGLE_PROJECT_ID: {os.getenv('GOOGLE_PROJECT_ID')}")
print(f"  - GOOGLE_REGION: {os.getenv('GOOGLE_REGION')}")
print(f"  - GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")

print("\n📡 测试 aisuite 调用 Vertex AI...")

try:
    import aisuite as ai
    client = ai.Client()

    print("✓ aisuite 客户端初始化成功")

    # 测试简单调用
    response = client.chat.completions.create(
        model="google:gemini-2.5-flash-lite",
        messages=[{"role": "user", "content": "Say 'Hello, World!' in one word."}],
        temperature=0,
    )

    result = response.choices[0].message.content
    print(f"✓ API 调用成功!")
    print(f"  响应: {result}")
    print("\n✅ 所有测试通过！可以运行 main.py")

except Exception as e:
    print(f"\n❌ 测试失败:")
    print(f"  错误类型: {type(e).__name__}")
    print(f"  错误信息: {str(e)}")
    print("\n💡 可能的解决方案:")
    print("  1. 检查代理是否正在运行（http://127.0.0.1:7897）")
    print("  2. 确认 Vertex AI 配置正确")
    print("  3. 检查网络连接")

print("\n" + "="*70)
