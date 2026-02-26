"""
主程序入口 - 运行反思模式SQL生成工作流
"""

import os
from dotenv import load_dotenv
from sql_workflow import run_workflow
import utils

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


def main():
    """主函数：配置并运行工作流"""

    # ============================================================================
    # 配置参数（可根据需要修改）
    # ============================================================================

    # 数据库路径
    db_path = "products.db"

    # 用户问题
    question = "哪种颜色的产品总销售额最高,以及对应的销售总额是多少？"

    # 模型配置
    # 支持的模型格式：
    # - Google Gemini: "google:gemini-2.0-flash-exp", "google:gemini-1.5-pro"
    # - OpenAI: "openai:gpt-4o", "openai:gpt-4o-mini"
    # - Anthropic: "anthropic:claude-3-5-sonnet-20241022"

    generation_model = "google:gemini-2.5-flash-lite"               # 用于生成V1 SQL的模型（快速）
    evaluation_model = "google:gemini-2.5-pro" # 用于反思和生成V2的模型（高质量）

    # ============================================================================
    # 创建数据库
    # ============================================================================

    print("\n🗄️  正在创建测试数据库...")
    utils.create_transactions_db(db_name=db_path)
    print()

    # ============================================================================
    # 运行工作流
    # ============================================================================

    result = run_workflow(
        db_path=db_path,
        question=question,
        generation_model=generation_model,
        evaluation_model=evaluation_model,
    )

    # ============================================================================
    # 输出结果摘要
    # ============================================================================

    if "error" in result:
        print(f"\n❌ 工作流执行出错：{result['error']}")
    else:
        print("\n📋 结果摘要：")
        print(f"  - V1 SQL：{result.get('sql_v1', 'N/A')}")
        print(f"  - V2 SQL：{result.get('sql_v2', 'N/A')}")
        print(f"  - 反思反馈：{result.get('feedback', 'N/A')}")
        print("\n💡 提示：对比 V1 和 V2 的执行结果，可以看到反思模式的改进效果！")


if __name__ == "__main__":
    main()
