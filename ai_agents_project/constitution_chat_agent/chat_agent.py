import random
from textwrap import dedent
from pydantic import Field

from agno.agent import Agent, AgentMemory
from agno.memory.db.sqlite import SqliteMemoryDb
from agno.models.openai import OpenAIChat
from agno.embedder.openai import OpenAIEmbedder
from agno.vectordb.mongodb import MongoDb
from agno.knowledge.langchain import LangChainKnowledgeBase
from agno.utils.pprint import pprint_run_response

from pymongo import MongoClient
import gridfs
import certifi

from langchain.schema import BaseRetriever

from pymongo import MongoClient
from rich.console import Console
from rich.prompt import Prompt


console = Console()


db_client = MongoClient(
    "mongodb+srv://<username>:<password>@<cluster>",
    tlsAllowInvalidCertificates=True,
    tlsCAFile=certifi.where(),
)
db = db_client["constitution"]
fs = gridfs.GridFS(db)


class MongoDbRetriever(BaseRetriever):
    vector_store: object = Field(
        ..., description="The MongoDB vector store instance"
    )  # Required field

    def __init__(self, vector_store):
        super().__init__(vector_store=vector_store)

    def _get_relevant_documents(self, query: str):
        # Use the vector_store's search method
        return self.vector_store.search(query)


vector_store = MongoDb(
    collection_name="constitution",
    client=db_client,
    embedder=OpenAIEmbedder(),
)

retriever = MongoDbRetriever(
    vector_store=vector_store,
)

knowledge_base = LangChainKnowledgeBase(vectorstore=vector_store, retriever=retriever)

session_id = random.randint(1, 1000000)

# def constitution_chat_agent(session_id: str):
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=knowledge_base,
    description="Constitution Chat Agent",
    memory=AgentMemory(
        db=SqliteMemoryDb(
            table_name="constitution_agent_memory",
            db_file="tmp/constitution_agent_memory.db",
        ),
        create_user_memories=True,
        create_session_summary=True,
    ),
    instructions=dedent(
        """
        You are a helpful assistant that provides information about the Constitution of the United States.
        You can answer questions, summarize sections, and provide explanations about the Constitution.

        Follow these steps to answer the user's question:
        1. Understand the user's question.
        2. First, search the knolwedge base for relevant documents.
        3. If the information is not found in the knowledge base or is not sufficient, search vector store.
        4. If you cannot find relevant information, do NOT search in OpenAI LLM. Respond with "Information Not Found".
        5. Provide a clear and concise answer to the user's question.
        """
    ),
    session_id=session_id,
    show_tool_calls=True,
    telemetry=True,
    debug_mode=True,
    monitoring=True,
    add_history_to_messages=True,
    num_history_responses=3,
    markdown=True,
)

if agent.knowledge is not None:
    agent.knowledge.load()


def upload_file_to_mongodb(file_path):
    """
    Uploads a file to MongoDB GridFS.
    :param file_path: Path to the file to be uploaded.
    :return: The ID of the uploaded file.
    """
    file_name = file_path.split("/")[-1]
    print(file_name)
    # Check if the file already exists in GridFS
    existing_file = fs.find_one({"filename": file_name})
    print(existing_file)
    if existing_file:
        print(f"File {file_name} already exists in GridFS with ID: {existing_file._id}")
        return existing_file._id
    else:
        with open(file_path, "rb") as file:
            file_id = fs.put(file, filename=file_name)
        print(f"File {file_name} uploaded to GridFS with ID: {file_id}")
        return file_id


def main():
    upload_file_to_mongodb("documents/concise_constitution.pdf")
    while True:
        message = Prompt.ask(
            "You: ",
            default="What is the Constitution Artle 1?",
            show_default=True,
        )
        if message.lower() in ["exit", "quit"]:
            break
        agent_response = agent.run(message, stream=True)
        pprint_run_response(agent_response)


if __name__ == "__main__":
    main()
