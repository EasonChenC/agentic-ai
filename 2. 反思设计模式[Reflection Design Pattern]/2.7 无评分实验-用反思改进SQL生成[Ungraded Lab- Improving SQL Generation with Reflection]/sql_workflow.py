"""
反思模式智能体工作流 - SQL生成
实现自我改进的SQL查询生成系统
"""

import json
import pandas as pd
import aisuite as ai
import utils

# 初始化 aisuite 客户端
client = ai.Client()


# ============================================================================
# 第1部分：SQL生成函数
# ============================================================================

def generate_sql(question: str, schema: str, model: str) -> str:
    """
    使用 LLM 将自然语言问题转换为 SQL 查询（第一版 V1）

    参数:
        question: 用户的自然语言问题
        schema: 数据库架构信息
        model: 使用的 LLM 模型名称

    返回:
        生成的 SQL 查询字符串
    """
    prompt = f"""
你是一名 SQL 助理。根据给定的数据库架构与用户问题，编写适用于 SQLite 的 SQL 查询。

架构：
{schema}

用户问题：
{question}

重要要求：
1. 仅返回纯SQL语句，不要包含任何解释文字
2. 不要使用Markdown代码块标记（不要```sql 或 ```）
3. 直接返回可执行的SQL代码
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


# ============================================================================
# 第2部分：反思评审函数
# ============================================================================

def refine_sql(
    question: str,
    sql_query: str,
    schema: str,
    model: str,
) -> tuple[str, str]:
    """
    基于 SQL 文本本身进行反思改进（无外部反馈）
    仅检查查询逻辑，不执行 SQL

    参数:
        question: 用户问题
        sql_query: 原始 SQL 查询
        schema: 数据库架构
        model: LLM 模型名称

    返回:
        (反馈文本, 改进后的SQL)
    """
    prompt = f"""
你是一位 SQL 审查与优化专家。

用户问题：
{question}

原始 SQL：
{sql_query}

表架构：
{schema}

步骤 1：简要评估 SQL 输出是否完整回答用户问题。
步骤 2：若需要改进，请提供适用于 SQLite 的优化版 SQL 查询。
若原始 SQL 已正确，请保持不变返回。

严格返回仅包含以下两个字段的 JSON：
{{
  "feedback": "<1-3 句解释问题或确认正确性>",
  "refined_sql": "<final SQL to run>"
}}
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    content = response.choices[0].message.content.strip()

    # 清理 Markdown 代码块标记
    content = content.replace("```json", "").replace("```", "").strip()

    try:
        obj = json.loads(content)
        feedback = str(obj.get("feedback", "")).strip()
        refined_sql = str(obj.get("refined_sql", sql_query)).strip()
        if not refined_sql:
            refined_sql = sql_query
    except Exception as e:
        # 若模型未返回有效 JSON 的回退处理
        print(f"⚠️  JSON解析失败: {e}")
        feedback = content.strip()
        refined_sql = sql_query

    return feedback, refined_sql


def refine_sql_external_feedback(
    question: str,
    sql_query: str,
    df_feedback: pd.DataFrame,
    schema: str,
    model: str,
) -> tuple[str, str]:
    """
    基于实际执行结果进行反思改进（有外部反馈）⭐核心函数
    这是反思模式的关键：使用真实执行结果来发现问题

    参数:
        question: 用户问题
        sql_query: 原始 SQL 查询
        df_feedback: SQL 执行后的实际结果（DataFrame）
        schema: 数据库架构
        model: LLM 模型名称

    返回:
        (反馈文本, 改进后的SQL V2)
    """
    prompt = f"""
你是一位 SQL 审查与优化专家。

用户问题：
{question}

原始 SQL：
{sql_query}

SQL 输出：
{df_feedback.to_markdown(index=False)}

表架构：
{schema}

步骤 1：简要评估该 SQL 输出是否回答了用户问题。
步骤 2：若可改进，请提供优化后的 SQL 查询。
若原始 SQL 已正确，请保持不变返回。

重要要求：
1. 仅返回纯JSON 对象，不要包含任何解释文字
2. 不要使用Markdown代码块标记（不要```json 或 ```）
3. 请严格返回仅包含以下两个字段的 JSON 对象：
- "feedback": 简短评估与建议
- "refined_sql": 需要执行的最终 SQL
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    content = response.choices[0].message.content.strip()

    # 清理 Markdown 代码块标记
    content = content.replace("```json", "").replace("```", "").strip()


    try:
        obj = json.loads(content)
        feedback = str(obj.get("feedback", "")).strip()
        refined_sql = str(obj.get("refined_sql", sql_query)).strip()
        if not refined_sql:
            refined_sql = sql_query
    except Exception as e:
        # 若模型未返回有效 JSON 的回退处理
        print(f"⚠️  JSON解析失败: {e}")
        print(f"原始内容: {content[:200]}...")
        feedback = content.strip()
        refined_sql = sql_query

    return feedback, refined_sql


# ============================================================================
# 第3部分：完整工作流函数
# ============================================================================

def run_workflow(
    db_path: str,
    question: str,
    generation_model: str,
    evaluation_model: str,
):
    """
    端到端自动化工作流：生成、执行、评估并改进 SQL 查询

    完整流程：
      1) 提取数据库架构
      2) 生成 SQL（V1）
      3) 执行 V1 → 展示输出
      4) 结合执行反馈反思 V1 → 提出改进版 SQL（V2）
      5) 执行 V2 → 展示最终答案

    参数:
        db_path: 数据库文件路径
        question: 用户的自然语言问题
        generation_model: 用于生成SQL的模型
        evaluation_model: 用于评估和改进的模型

    返回:
        包含所有产物（SQL、反馈、结果）的字典
    """
    print("\n" + "="*70)
    print("🚀 启动 SQL 反思工作流")
    print("="*70)
    print(f"\n❓ 用户问题: {question}\n")

    # 1) 提取数据库架构
    print("📘 步骤 1：提取数据库架构...")
    schema = utils.get_schema(db_path)
    print(f"✓ 架构提取成功")
    print(f"  {schema}")
    print()

    # 2) 生成 SQL（V1）
    print("🧠 步骤 2：生成 SQL（V1）...")
    print(f"  使用模型：{generation_model}")
    sql_v1 = generate_sql(question, schema, generation_model)
    print(f"✓ V1生成成功")
    print(f"  SQL: {sql_v1}")
    print()

    # 3) 执行 V1
    print("🧪 步骤 3：执行 V1（SQL 输出）...")
    df_v1 = utils.execute_sql(sql_v1, db_path)
    print(f"✓ V1执行完成")
    print(df_v1)
    print()

    # 4) 结合执行反馈反思 V1 → 提出改进版 SQL（V2）
    print("🧭 步骤 4：反思 V1（基于执行结果的反馈）...")
    print(f"  使用模型：{evaluation_model}")
    feedback, sql_v2 = refine_sql_external_feedback(
        question=question,
        sql_query=sql_v1,
        df_feedback=df_v1,  # 外部反馈：V1 的执行结果
        schema=schema,
        model=evaluation_model,
    )
    print(f"✓ 反思完成")
    print(f"  反馈: {feedback}")
    print()

    print("🔁 步骤 5：改进后的 SQL（V2）...")
    print(f"  SQL: {sql_v2}")
    print()

    # 5) 执行 V2 → 展示最终答案
    print("✅ 步骤 6：执行 V2（最终答案）...")
    df_v2 = utils.execute_sql(sql_v2, db_path)
    print(f"✓ V2执行完成")
    print(df_v2)
    print()

    print("="*70)
    print("🎉 工作流完成！")
    print("="*70)

    return {
        "sql_v1": sql_v1,
        "result_v1": df_v1,
        "feedback": feedback,
        "sql_v2": sql_v2,
        "result_v2": df_v2,
    }
