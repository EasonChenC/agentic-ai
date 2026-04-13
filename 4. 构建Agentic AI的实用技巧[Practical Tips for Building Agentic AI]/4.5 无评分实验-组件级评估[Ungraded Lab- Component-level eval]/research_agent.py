"""Research agent with tool calling capabilities."""

from datetime import datetime
from aisuite import Client
import research_tools


def find_references(
    task: str,
    model: str = "google:gemini-2.5-flash-lite",
    return_messages: bool = False
):
    """
    Execute a research task using external tools (arxiv, tavily, wikipedia).

    Args:
        task (str): The research task description
        model (str): Model identifier for AISuite (default: Gemini)
        return_messages (bool): If True, return (content, messages) tuple

    Returns:
        str or tuple: Research results, optionally with message history
    """

    # Initialize AISuite client
    client = Client()

    # Construct prompt with current date context
    prompt = f"""
    You are a research function with access to:
    - arxiv_search_tool: Academic papers
    - tavily_search_tool: General web search (return JSON when needed)
    - wikipedia_search_tool: Encyclopedia-style summaries

    IMPORTANT: When calling tools, always include all required parameters.
    - For arxiv_search_tool, set "query" to your search keywords.
    - For tavily_search_tool, set "query" to your search keywords.
    - For wikipedia_search_tool, set "query" to the topic you want to search.

    CRITICAL: In your final response, you MUST include the full URLs from the tool results.
    Format your response like this:
    - Paper/Article Title: [brief description]
      URL: https://example.com/full-url

    Always cite sources with their complete URLs so they can be evaluated.

    Task:
    {task}

    Today is {datetime.now().strftime('%Y-%m-%d')}.
    """.strip()

    messages = [{"role": "user", "content": prompt}]

    # Define available tools with both definitions and implementations
    tools = [
        research_tools.arxiv_search_tool,
        research_tools.tavily_search_tool,
        research_tools.wikipedia_search_tool,
    ]

    try:
        # Call model with tool support
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_turns=5,  # Allow multiple tool calling rounds
        )

        content = response.choices[0].message.content

        if return_messages:
            return content, messages
        return content

    except Exception as e:
        error_msg = f"[Model Error: {e}]"
        if return_messages:
            return error_msg, messages
        return error_msg
