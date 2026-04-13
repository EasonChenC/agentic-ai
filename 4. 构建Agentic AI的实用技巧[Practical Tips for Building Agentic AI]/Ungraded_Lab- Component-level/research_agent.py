# _*_ coding : utf-8 _*_
# @Time : 2026/2/13 10:42
# @Author : Eason_Chen
# @File : research_agent
# @Project : Ungraded_Lab- Component-level
from datetime import datetime
from aisuite import Client
import research_tools

def find_reference(
  task: str,
  model: str = "",
  return_messages: bool = False
):
    """
    Execute a research task using external tools(arxiv, tavily,wikipedia).

    Args:
        task (str): The research task description.
        model (str): Model identifier for AISuite (default: Gemini)
        return_messages (bool): If True, return (Content, messages) tuple

    Returns:
        str or tuple: Research results,optionally with message history.
    """
    client = Client()

    prompt = f"""
    You are a research function with access to:
    - arxiv_search_tool: Academic papers,
    - tavily_search_tool: General web search (return JSON when needed)
    - wikipedia_search_tool:  Encyclopedia-style summaries
    
    important: when calling tools,always include all required parameters.
    - For arxiv_search_tool, set "query" to your search keywords
    - For tavily_search_tool, set "query" to your search keywords.
    - For wikipedia_search_tool, set "query" to the topic you want to search.
    
    CRITICAL: In your final response, you must include the full URLS from the tool results.
    Format your response like this:
    - Paper/Article Title: [brief description]
      URL: https://example.com/full-url
      
    Always cite sources with their complete URLs so they can be evaluated.
    
    Task:
    {task}
    
    Today is {datetime.now().strftime('%Y-%m-%d')}. 
    """.strip()

    messages = [{"role": "user", "content": prompt}]

    tools = [
        research_tools.arxiv_search_tool,
        research_tools.tavily_search_tool,
        research_tools.wikipedia_search_tool
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_turns=5
        )

        content = response.choices[0].message.content

        if return_messages:
            return content,messages
        return content

    except Exception as e:
        error_msg = f"[Model Error: {e}]"
        if return_messages:
            return error_msg, messages
        return error_msg