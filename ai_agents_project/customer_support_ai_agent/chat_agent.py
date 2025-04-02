import json

from enum import Enum
from typing import Iterator
from agno.agent import Agent, AgentMemory
from agno.embedder.openai import OpenAIEmbedder
from agno.memory.db.sqlite import SqliteMemoryDb
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage

# from agno.tools.duckduckgo import DuckDuckGoTools
from agno.utils.pprint import pprint_run_response
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.json import JSONKnowledgeBase
from agno.workflow import Workflow, RunResponse

from rich.console import Console
from rich.panel import Panel
from rich.json import JSON
from rich.prompt import Prompt

from pydantic import BaseModel


chat_agent_storage = SqliteStorage(
    table_name="chat_agent_memories",
    db_file="tmp/chat_agent_memories.db",
    auto_upgrade_schema=True,
)


class SentimentTypes(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class CategoryTypes(Enum):
    TECHNICAL = "technical"
    FINANCIAL = "financial"
    GENERAL = "general"


class State(BaseModel):
    query: str
    query_category: CategoryTypes
    sentiment: SentimentTypes
    response: str


class Categorize(BaseModel):
    state: State


class Analyze(BaseModel):
    state: State


class Respond(BaseModel):
    state: State


class Escalate(BaseModel):
    state: State


class CustomerSupportAgent(Workflow):
    description = "Customer Support AI Agent that categorizes, analyzes, responds, and escalates (human) customer queries"

    categorize_agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        # tools=[DuckDuckGoTools()],
        description="Categorize the customer query.",
        instructions="""
            You are a AI agent expert at categorizing customer queries.
            Your correct categorization will help the AI agent team to provide the best response.
            Categories: technical, financial, general
        """,
        knowledge=JSONKnowledgeBase(
            path="./knowledge/categories.json",
            vector_db=LanceDb(
                table_name="query_categories",
                embedder=OpenAIEmbedder(id="text-embedding-3-small"),
            ),
        ),
        show_tool_calls=True,
        markdown=True,
        response_model=Categorize,
    )

    analyze_agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        # tools=[DuckDuckGoTools()],
        description="Analyze the customer query for sentiment",
        instructions="""
            You are a AI agent expert at analyzing customer queries.
            Your sentiment analysis will help the AI agent team to provide the best response.
            Sentiments: positive, negative, neutral
            Positive sentiment means the customer is happy, satisfied or pleased ex: Thank you for your  service.
            Neutral sentiment means the customer has query ex: What is stock value of?.
            Negative sentiment means the customer is unhappy, frustrated or angry. ex: I am frustrated with your service. 
        """,
        show_tool_calls=True,
        knowledge=JSONKnowledgeBase(path="./knowledge/sentiment.json"),
        markdown=True,
        response_model=Analyze,
    )

    respond_agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        # tools=[DuckDuckGoTools()],
        description="Respond to the customer query.",
        instructions="""
            You are a AI agent expert at responding to customer queries with excellent memoory.
            - Your response should be profeesional and helpful.
            - Keep your responses brief and to the point.
            - Your respond should be relevant to customer's `query_category` and consider customer's `sentiment`.
            - Store current session conversation in memory.
        """,
        show_tool_calls=True,
        storage=chat_agent_storage,
        memory=AgentMemory(
            db=SqliteMemoryDb(
                table_name="chat_agent_memory", db_file="tmp/chat_agent_memory.db"
            ),
            create_session_summary=True,
            create_user_memories=True,
            update_user_memories_after_run=True,
            update_session_summary_after_run=True,
        ),
        markdown=True,
        response_model=Respond,
    )

    escalate_agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        # tools=[DuckDuckGoTools()],
        description="Escalate the customer query to a human agent.",
        instructions="""
            You are a AI agent expert at escalating customer queries.
            Your escalation should be timely and appropriate.
            Provide a brief summary of the customer query.
        """,
        show_tool_calls=True,
        markdown=True,
        response_model=Escalate,
    )

    def run(self, query: str) -> Iterator[RunResponse]:
        """
        Run the Customer Support AI Agent workflow with the given query.

        This function orchestrates the workflow of the Customer Support AI Agent.

        Args:
            query (str): The customer query to process.

        Returns:
            Iterator[RunResponse]: The responses from each agent in the workflow

        Steps:
        1. Categorize the customer query.
        2. Analyze the sentiment of the categorized query.
        3. If the sentiment is negative, escalate the query.
        4. Otherwise, respond to the query.
        """
        # session_id = self.session_id
        sentiment: SentimentTypes = self.analyze_agent.run(
            query
        ).content.state.sentiment
        print(f"Sentiment: {sentiment}")
        if sentiment == SentimentTypes.NEGATIVE:
            yield self.escalate_agent.run(query=query)

        category: CategoryTypes = self.categorize_agent.run(
            query
        ).content.state.query_category
        print(f"Category: {category}")
        response = self.respond_agent.run(query).content.state.response
        print(f"Response: {response}")


def print_agent_memory(agent):
    """Print the current state of agent's memory systems"""
    console = Console()

    # Print chat history
    console.print(
        Panel(
            JSON(
                json.dumps([m.to_dict() for m in agent.memory.messages]),
                indent=4,
            ),
            title=f"Chat History for session_id: {agent.session_id}",
            expand=True,
        )
    )

    # Print user memories
    console.print(
        Panel(
            JSON(
                json.dumps(
                    [
                        m.model_dump(include={"memory", "input"})
                        for m in agent.memory.memories
                    ]
                ),
                indent=4,
            ),
            title=f"Memories for user_id: {agent.user_id}",
            expand=True,
        )
    )


if __name__ == "__main__":
    session_id = "user_1"
    while True:
        message = Prompt.ask("Enter a customer query:")
        if message == "exit":
            break
        agent = CustomerSupportAgent(
            session_id=f"customer_support_agent_{session_id}",
            name="Customer Support AI Agent",
        )

        run_workflow: Iterator[RunResponse] = agent.run(query=message)

        pprint_run_response(run_workflow)

        print_agent_memory(agent.respond_agent)
