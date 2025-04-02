from textwrap import dedent
from typing import Iterator, List

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.sql import SQLTools
from agno.workflow import RunResponse

from pydantic import BaseModel
from rich.prompt import Prompt
from rich.console import Console

console = Console()


class Order(BaseModel):
    orderId: str
    productId: str
    customerId: str
    orderDate: str
    orderStatus: str
    orderAmount: float


class Orders(BaseModel):
    orders: List[Order]


agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[
        SQLTools(
            db_url="sqlite:////Users/thisisnish/mytestdb.db",
        )
    ],
    description="SQL Query Agent that runs SQL queries on a database",
    response_model=Orders,
    instructions=dedent(
        """
        You are a SQL Query Agent. You can run SQL queries on a database.
        Given the user input, you need to run the SQL query on the database and return the results.
        Use SQLTools to interact with the database:
            1. list_tables, if not sure which table to query
            2. describe_table, to get the schema of the table
            3. run_sql_query, to run the SQL query
        
        Example:
        input: "give me all orders from this month"
        sql_query: "SELECT * FROM orders WHERE orderDate >= '2022-01-01' AND orderDate <= '2022-01-31'"
        output: "Here are all the orders from this month: ..."
        """
    ),
    show_tool_calls=True,
    markdown=True,
)


def main():
    console.print("Welcome to the SQL Query Agent!")
    message = Prompt.ask(
        "Ask a question to the SQL Query Agent:",
        default="Give me all orders from this month",
    )
    agent_response = agent.run(message)
    for order in agent_response.content.orders:
        console.print(order.model_dump())


if __name__ == "__main__":
    main()
