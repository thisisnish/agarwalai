from agent import chain_with_history
session_id = "user_123"


response1 = chain_with_history.invoke(
    {"input": "Hello! How are you?"},
    config={"configurable": {"session_id": session_id}}
)
print("AI:", response1.content)

response2 = chain_with_history.invoke(
    {"input": "What was my previous message?"},
    config={"configurable": {"session_id": session_id}}
)
print("AI:", response2.content)
