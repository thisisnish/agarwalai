""" 
Trello Reasonong Agent - Think, Reason and Create a Plan
This agent uses the Trello API to create a board, lists, and cards based on the user's input.

Setup:
1. Install the required libraries:
   uv pip install requirements.txt
2. Create a Trello API key and token:
   - Go to https://trello.com/app-key and generate an API key.
   - Generate a token using the API key.
3. Set the environment variables:
   - TRELLO_API_KEY: Your Trello API key
   - TRELLO_API_TOKEN: Your Trello API token
4. Run the agent:
   - python trello_agent.py
5. Follow the prompts to create a Trello board, lists, and cards.

"""

import asyncio
from textwrap import dedent
import os

from agno.agent import Agent
from agno.models.openai import OpenAIChat
# from agno.tools.mcp import MCPTools
from agno.utils.log import log_error, log_exception, log_info
from agno.utils.pprint import pprint_run_response
from agno.tools.trello import TrelloTools
from agno.tools.reasoning import ReasoningTools
from agno.playground import Playground, serve_playground_app
import dotenv

from rich.console import Console
from pydantic import BaseModel


console = Console()


dotenv.load_dotenv()



class TrelloAgent(BaseModel):
    query: str
    response: str



# def run_agent(msg) -> None:
trello_thinking_agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[TrelloTools(
        api_key=os.getenv("TRELLO_API_KEY"),
        api_secret=os.getenv("TRELLO_API_SECRET"),
        token=os.getenv("TRELLO_API_TOKEN"),
    ), 
        ReasoningTools(
            add_instructions=True,
            add_few_shot=True,
            instructions=dedent(
                """
                You are a reasoning agent. Your job is to think, reason and create a plan based on the user's input.
                You can also use tools to perform tasks and get information.
                """
            )
        )
    ],
    instructions=dedent(
        """
        You are a reasoning agent. Your job is to think, reason and create a plan based on the user's input.
        You can also use tools to perform tasks and get information.
        """
    ),
    debug_mode=True,
    show_tool_calls=True,
    telemetry=True,
    monitoring=True,
    markdown=True,
    response_model=TrelloAgent,
    num_history_responses=5,
    stream=True,
    reasoning=True,
)

def main():
    while True:
        try:
            msg = input("Enter your message: ")
            if msg.lower() == "exit":
                break
            agent_response = trello_thinking_agent.run(msg, stream=True)
            console.print(agent_response.content.model_dump())
            # print(f"Agent response: {agent_response}")
        except Exception as e:
            log_exception(e)
            log_error(f"Error: {e}")


app = Playground(agents=[trello_thinking_agent]).get_app()

if __name__ == "__main__":
    console.print("Starting Trello Agent...")
    # serve_playground_app("trello_agent:app", reload=True)
    main()
