from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from context import Context

stream_mode = True
model = OllamaLLM(model="qwen2.5:7b")

template = """
You are a helpful assistant in Choreo, an iPaaS by WSO2. Answer the question based on the context provided.
If the context does not contain enough information to answer the question, respond with "I don't know".

Here is the context:
{context}

Here is the question:
{question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

while True:
    print("-" * 30)
    user_input = input("Enter your question (or type '/exit' to quit): ")
    if user_input.lower() == '/exit':
        break
    
    print("Assistant: ")
    if stream_mode:
        for chunk in chain.stream({
            "context": Context.what_is_choroe,
            "question": user_input
        }):
            print(chunk, end='', flush=True)
        print()
    else:
        result = chain.invoke({
            "context": Context.what_is_choroe,
            "question": user_input
        })
        print(result)