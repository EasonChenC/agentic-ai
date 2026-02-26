"""
测试Gemini API配置（使用新SDK）
"""

import os
from dotenv import load_dotenv
from google import genai

# 加载环境变量
load_dotenv()

def test_gemini_api():
    """测试Gemini API是否正确配置"""

    print("🧪 开始测试Gemini API配置...\n")

    # 1. 检查API密钥
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ 错误：未找到GOOGLE_API_KEY环境变量")
        print("   请在.env文件中配置：GOOGLE_API_KEY=your_key_here")
        return False

    print(f"✓ API密钥已配置：{api_key[:10]}...{api_key[-4:]}")

    # 2. 初始化Gemini客户端
    try:
        client = genai.Client(api_key=api_key)
        print("✓ Gemini客户端初始化成功")
    except Exception as e:
        print(f"❌ Gemini客户端初始化失败：{e}")
        return False

    # 3. 测试文本生成
    print("\n📝 测试文本生成...")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=["用一句话介绍Python编程语言"],
            config=genai.types.GenerateContentConfig(
                temperature=0.7
            )
        )
        print(f"✓ 文本生成成功")
        print(f"  响应：{response.text[:100]}...")
    except Exception as e:
        print(f"❌ 文本生成失败：{e}")
        return False

    # 4. 测试多模态能力
    print("\n🖼️  测试多模态能力...")
    try:
        from PIL import Image

        # 创建一个简单的测试图像
        test_image = Image.new('RGB', (100, 100), color='red')

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[test_image, "描述这张图片的颜色"],
            config=genai.types.GenerateContentConfig(
                temperature=0.1
            )
        )
        print(f"✓ 多模态生成成功")
        print(f"  响应：{response.text[:100]}...")
    except Exception as e:
        print(f"❌ 多模态生成失败：{e}")
        return False

    print("\n" + "="*70)
    print("✅ 所有测试通过！Gemini API配置正确")
    print("="*70)
    return True


if __name__ == "__main__":
    test_gemini_api()
