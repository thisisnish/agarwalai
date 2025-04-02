from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools


agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    description="You are an enthusiatic cricket fan with a flair of storytelling of close games.",
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response(
    "Tell me about ICC Champions Trophy 2025 final match.", stream=True
)
