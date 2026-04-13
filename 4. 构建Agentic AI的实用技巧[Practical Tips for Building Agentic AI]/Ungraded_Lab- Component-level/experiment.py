# _*_ coding : utf-8 _*_
# @Time : 2026/2/13 11:10
# @Author : Eason_Chen
# @File : experiment
# @Project : Ungraded_Lab- Component-level

import json
from dotenv import load_dotenv
from research_agent import find_reference
from utils import print_html, evaluate_tavily_results
from config import TOP_DOMAINS, MIN_RATIO, MODEL_NAME, DEFAULT_RESEARCH_TASK
import os
# Load environment variables (API keys, proxy settings)
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


def run_experiment(
    topic: str = None,
    min_ratio: float = None,
    show_domains :  bool = True
):
    """
    Run component-level evaluation experiment.

    Args:
        topic (str): Research topic (uses default if None)
        min_ratio (float): Minimum ratio for passing (uses config default if None)
        show_domains (bool): Whether to display TOP_DOMAINS list
    """
    # Use defaults from config if not provided
    if topic is None:
        research_task = DEFAULT_RESEARCH_TASK
        topic = "latest advances in black hole science"
    else:
        research_task = f"Find 2-3 key papers and reliable reviews on {topic}."

    if min_ratio is None:
        min_ratio = MIN_RATIO

    print(f"\n{'='*60}")
    print(f"Component-Level Evaluation Experiment")
    print(f"Model: {MODEL_NAME}")
    print(f"Topic: {topic}")
    print(f"Min Ratio: {min_ratio:.0%}")
    print(f"{'='*60}\n")

    # Step 1: Display preferred domains (optional)
    if show_domains:
        domains_sample = sorted(list(TOP_DOMAINS))[:8]
        print_html(
            json.dumps(domains_sample, indent=2),
            title="<h3>Preferred Domains (Sample)</h3>"
        )

    # Step 2: Execute research
    print(f"\n🔍 Executing research task...")
    research_output = find_references(research_task, model=MODEL_NAME)

    # Debug: Print raw output to see what the model returned
    print(f"\n[DEBUG] Raw research output length: {len(research_output)} characters")
    print(f"[DEBUG] First 500 characters:\n{research_output[:500]}\n")

    print_html(
        research_output,
        title=f"<h3>Research Results: {topic}</h3>"
    )

    # Step 3: Evaluate results
    print(f"\n📊 Evaluating source quality...")
    flag, eval_report = evaluate_tavily_results(
        TOP_DOMAINS,
        research_output,
        min_ratio=min_ratio
    )

    print_html(
        "<pre>" + eval_report + "</pre>",
        title="<h3>Evaluation Summary</h3>"
    )

    # Step 4: Summary
    status = "✅ PASSED" if flag else "❌ FAILED"
    print(f"\n{'='*60}")
    print(f"Evaluation Result: {status}")
    print(f"{'='*60}\n")

    return {
        "topic": topic,
        "model": MODEL_NAME,
        "passed": flag,
        "research_output": research_output,
        "evaluation_report": eval_report
    }