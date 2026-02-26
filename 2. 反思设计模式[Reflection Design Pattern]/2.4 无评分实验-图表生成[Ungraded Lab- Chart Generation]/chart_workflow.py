"""
反思模式智能体工作流 - 图表生成
实现自我改进的数据可视化生成系统
"""

import re
import json
import utils

# ============================================================================
# 第1部分：代码生成函数
# ============================================================================

def generate_chart_code(instruction: str, model: str, out_path_v1: str) -> str:
    """
    生成使用 matplotlib 绘图的 Python 代码，并用标签包裹返回。

    参数:
        instruction: 用户对图表的需求描述
        model: 使用的LLM模型名称
        out_path_v1: 图表保存路径

    返回:
        包含在 <execute_python> 标签中的代码字符串
    """

    prompt = f"""
    你是一位数据可视化专家。

    请*严格*按以下格式返回你的答案：

    <execute_python>
    # 在此填写有效的 Python 代码
    </execute_python>

    不要添加任何解释，仅包含上述标签与代码。

    ⚠️ 重要：DataFrame 'df' 已经存在并包含真实数据，其列包括：
    - date (M/D/YY)
    - time (HH:MM)
    - cash_type (card 或 cash)
    - card (string)
    - price (number)
    - coffee_name (string)
    - quarter (1-4)
    - month (1-12)
    - year (YYYY)

    用户指令：{instruction}

    代码要求：
    1. **直接使用已存在的 'df' 变量**，它已经加载了真实数据。
    2. **严禁创建示例数据**，不要使用 pd.DataFrame() 创建新的 df。
    3. **严禁重新定义 df 变量**，不要有任何 df = ... 的赋值语句。
    4. 使用 matplotlib 进行绘图。
    5. 添加清晰的标题、坐标轴标签，并在需要时添加图例。
    6. 将图像以 '{out_path_v1}' 保存，dpi=300。
    7. 不要调用 plt.show()。
    8. 使用 plt.close() 关闭所有图。
    9. 补充所有必要的 import 语句（pandas, matplotlib 等）。

    仅返回包含在 <execute_python> 标签中的代码。不要包含任何注释说明需要加载数据。
    """

    response = utils.get_response(model, prompt)
    return response


# ============================================================================
# 第2部分：反思评审函数
# ============================================================================

def reflect_on_image_and_regenerate(
    chart_path: str,
    instruction: str,
    model_name: str,
    out_path_v2: str,
    code_v1: str,
) -> tuple[str, str]:
    """
    根据给定指令评审图表图像与原始代码，然后返回改进后的 matplotlib 代码。

    参数:
        chart_path: V1图表的文件路径
        instruction: 用户的原始需求
        model_name: 使用的LLM模型名称
        out_path_v2: V2图表的保存路径
        code_v1: V1的原始代码（提供上下文）

    返回:
        (feedback, refined_code_with_tags) 元组
        - feedback: 对V1的反思反馈
        - refined_code_with_tags: 改进后的代码（包含标签）
    """
    # 将图表编码为base64
    media_type, b64 = utils.encode_image_b64(chart_path)

    prompt = f"""
    你是一位数据可视化专家。
    你的任务：依据给定指令评审附件中的图表与原始代码，
    并返回改进后的 matplotlib 代码。

    原始代码（用于提供上下文）：
    {code_v1}

    输出格式（严格遵守！）：
    1) 第一行：仅包含 "feedback" 字段的有效 JSON 对象。
    示例：{{"feedback": "图例不清晰，且坐标轴标签存在重叠。"}}

    2) 换行后，仅输出用如下标签包裹的改进版 Python 代码：
    <execute_python>
    ...
    </execute_python>

    3) 在代码中导入所有必要的库。不要依赖原始代码中的 import。

    强约束：
    - 除上述两部分外，不要包含 Markdown、反引号或任何额外说明文字。
    - 仅使用 pandas/matplotlib（不使用 seaborn）。
    - **DataFrame 'df' 已经存在并包含真实数据**，直接使用它。
    - **严禁创建示例数据**，不要使用 pd.DataFrame() 创建新的 df。
    - **严禁重新定义 df 变量**，不要有任何 df = ... 的赋值语句。
    - 不要从文件读取数据（df 已加载）。
    - 保存到 '{out_path_v2}'，dpi=300。
    - 结尾始终调用 plt.close()（不要使用 plt.show()）。
    - 包含所有必要的 import 语句。

    架构（df 中可用的列）：
    - date (M/D/YY)
    - time (HH:MM)
    - cash_type (card 或 cash)
    - card (string)
    - price (number)
    - coffee_name (string)
    - quarter (1-4)
    - month (1-12)
    - year (YYYY)

    指令：
    {instruction}
    """

    # 根据模型类型选择调用方式
    lower = model_name.lower()
    if "claude" in lower or "anthropic" in lower:
        content = utils.image_anthropic_call(model_name, prompt, media_type, b64)
    elif "gemini" in lower:
        content = utils.image_gemini_call(model_name, prompt, media_type, b64)
    else:
        content = utils.image_openai_call(model_name, prompt, media_type, b64)

    # 解析第一行的JSON反馈
    lines = content.strip().splitlines()
    json_line = lines[0].strip() if lines else ""

    try:
        obj = json.loads(json_line)
    except Exception as e:
        # 回退：尝试在完整内容中捕获第一个 {...}
        m_json = re.search(r"\{.*?\}", content, flags=re.DOTALL)
        if m_json:
            try:
                obj = json.loads(m_json.group(0))
            except Exception as e2:
                obj = {"feedback": f"Failed to parse JSON: {e2}", "refined_code": ""}
        else:
            obj = {"feedback": f"Failed to find JSON: {e}", "refined_code": ""}

    # 从 <execute_python>...</execute_python> 中提取改进代码
    m_code = re.search(r"<execute_python>([\s\S]*?)</execute_python>", content)
    refined_code_body = m_code.group(1).strip() if m_code else ""
    refined_code = utils.ensure_execute_python_tags(refined_code_body)

    feedback = str(obj.get("feedback", "")).strip()
    return feedback, refined_code


# ============================================================================
# 第3部分：完整工作流函数
# ============================================================================

def run_workflow(
    dataset_path: str,
    user_instructions: str,
    generation_model: str,
    reflection_model: str,
    image_basename: str = "chart",
):
    """
    端到端流水线：
      1) 加载数据集
      2) 生成 V1 代码
      3) 执行 V1 → 生成 chart_v1.png
      4) 反思 V1（图像 + 原始代码）→ 反馈 + 改进代码
      5) 执行 V2 → 生成 chart_v2.png

    参数:
        dataset_path: CSV数据文件路径
        user_instructions: 用户对图表的需求描述
        generation_model: 用于生成V1代码的模型
        reflection_model: 用于反思和生成V2的模型
        image_basename: 图表文件的基础名称

    返回:
        包含所有产物（代码、反馈、图像路径）的字典
    """
    print("\n" + "="*70)
    print("🚀 启动反思模式智能体工作流")
    print("="*70)

    # 0) 加载数据集
    print("\n📊 步骤 0：加载数据集...")
    df = utils.load_and_prepare_data(dataset_path)
    print(f"✓ 数据集加载成功：{len(df)} 行数据")
    print(f"  列名：{', '.join(df.columns.tolist())}")

    # 图表保存路径
    out_v1 = f"{image_basename}_v1.png"
    out_v2 = f"{image_basename}_v2.png"

    # 1) 生成代码 (V1)
    print(f"\n📝 步骤 1：生成绘图代码（V1）...")
    print(f"  使用模型：{generation_model}")
    code_v1 = generate_chart_code(
        instruction=user_instructions,
        model=generation_model,
        out_path_v1=out_v1,
    )
    print(f"✓ V1代码生成成功（{len(code_v1)} 字符）")

    # 2) 执行 V1
    print(f"\n💻 步骤 2：执行绘图代码（V1）...")
    match = re.search(r"<execute_python>([\s\S]*?)</execute_python>", code_v1)
    if match:
        initial_code = match.group(1).strip()
        exec_globals = {"df": df}
        try:
            exec(initial_code, exec_globals)
            print(f"✓ V1图表生成成功：{out_v1}")
        except Exception as e:
            print(f"✗ V1代码执行失败：{e}")
            return {"error": str(e)}
    else:
        print("✗ 未找到可执行代码标签")
        return {"error": "No executable code found"}

    # 3) 对 V1 进行反思
    print(f"\n🔍 步骤 3：对 V1 进行反思...")
    print(f"  使用模型：{reflection_model}")
    feedback, code_v2 = reflect_on_image_and_regenerate(
        chart_path=out_v1,
        instruction=user_instructions,
        model_name=reflection_model,
        out_path_v2=out_v2,
        code_v1=code_v1,
    )
    print(f"✓ 反思完成")
    print(f"  反馈：{feedback[:100]}..." if len(feedback) > 100 else f"  反馈：{feedback}")

    # 4) 执行 V2
    print(f"\n🎨 步骤 4：执行改进后的绘图代码（V2）...")
    match = re.search(r"<execute_python>([\s\S]*?)</execute_python>", code_v2)
    if match:
        reflected_code = match.group(1).strip()
        exec_globals = {"df": df}
        try:
            exec(reflected_code, exec_globals)
            print(f"✓ V2图表生成成功：{out_v2}")
        except Exception as e:
            print(f"✗ V2代码执行失败：{e}")
            return {
                "code_v1": code_v1,
                "chart_v1": out_v1,
                "feedback": feedback,
                "error_v2": str(e)
            }
    else:
        print("✗ 未找到可执行代码标签")

    print("\n" + "="*70)
    print("✅ 工作流完成！")
    print("="*70)

    return {
        "code_v1": code_v1,
        "chart_v1": out_v1,
        "feedback": feedback,
        "code_v2": code_v2,
        "chart_v2": out_v2,
    }
