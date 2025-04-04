# Constitution AI Agent

## This chat AI Agent answers questions regarding the constition of the US. The Agent only searches in existing knowledge base. If irrelevent question is asked the agent replies No Information Found.

### Concepts used:

1. Session memory management
2. Knowledge management for quick accces to information
3. Document retrival using chunks
4. Log usage for analytics

### Future extensions

1. Summarize session context, when it gets too long
2. Token-bounded contecxt window

### Tech Stack

1. Agno for Agent
2. OpenAI for LLM
3. MongoDB for document storage

### How to use

Note: Update MongoDB Client URI
```
pip install -3 requirements.txt

python chat_agent.py
````
