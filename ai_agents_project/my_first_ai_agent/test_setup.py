import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
# Load environment variables
load_dotenv() 
# Initialize the ChatOpenAI instance 
llm = ChatOpenAI(model="gpt-4o-mini") 
# Test the setup 
response = llm.invoke("Hello! Are you working?")
print(response.content)
