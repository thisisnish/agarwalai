from agno.agent import Agent
from agno.models.openai import OpenAIChat


agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    description="You are an enthusiatic cricket fan with a flair of storytelling of close games.",
    markdown=True
)
agent.print_response("Tell me about todays IPL game between RCB and CSK,", stream=True)
