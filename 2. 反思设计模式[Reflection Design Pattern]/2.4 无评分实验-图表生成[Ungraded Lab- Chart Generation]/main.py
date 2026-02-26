"""
主程序入口 - 运行反思模式智能体工作流
"""

from dotenv import load_dotenv
from chart_workflow import run_workflow
import utils

# 加载环境变量
load_dotenv()


def main():
    """主函数：配置并运行工作流"""

    # ============================================================================
    # 配置参数（可根据需要修改）
    # ============================================================================

    # 数据集路径
    dataset_path = "coffee_sales.csv"

    # 用户需求描述
    user_instructions = "使用 coffee_sales.csv 中的数据，创建一张对比 2024 与 2025 年第一季度不同咖啡类型销售的图表。"

    # 模型配置
    # 支持的模型：
    # - OpenAI: gpt-4o, gpt-4o-mini, gpt-3.5-turbo
    # - Anthropic: claude-3-opus, claude-3-sonnet
    # - Google: gemini-1.5-pro, gemini-1.5-flash

    generation_model = "gemini-2.5-flash-lite"  # 用于生成V1代码的模型（快速）
    reflection_model = "gemini-2.5-flash"    # 用于反思和生成V2的模型（高质量）

    # 图表文件名前缀
    image_basename = "coffee_chart"

    # ============================================================================
    # 运行工作流
    # ============================================================================

    result = run_workflow(
        dataset_path=dataset_path,
        user_instructions=user_instructions,
        generation_model=generation_model,
        reflection_model=reflection_model,
        image_basename=image_basename
    )

    # ============================================================================
    # 输出结果摘要
    # ============================================================================

    if "error" in result:
        print(f"\n❌ 工作流执行出错：{result['error']}")
    else:
        print("\n" + "="*70)
        print("📊 工作流执行完成！以下是详细结果：")
        print("="*70)

        # 展示反思反馈
        utils.print_html(
            result.get('feedback', 'N/A'),
            title="💭 反思反馈"
        )

        # 展示V1图表
        utils.print_html(
            result.get('chart_v1', 'N/A'),
            title="📈 初始版本图表（V1）",
            is_image=True
        )

        # 展示V2图表
        utils.print_html(
            result.get('chart_v2', 'N/A'),
            title="✨ 改进版本图表（V2）",
            is_image=True
        )

        print("\n💡 提示：对比上方两张图表，查看反思模式带来的改进效果！")


if __name__ == "__main__":
    main()
