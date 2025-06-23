from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pprint import pprint

from context import Context
from vector import retriever

stream_mode = True
model = OllamaLLM(model="qwen2.5:7b")

template = """
You are a helpful assistant. Answer the question based on the context provided.
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
    question = input("Enter your question (or type '/exit' to quit): ")
    if question.lower() == '/exit':
        break

    context = retriever.invoke(question)
    print("Context retrieved:")
    pprint(context)
    print("Assistant: ")
    if stream_mode:
        for chunk in chain.stream({
            "context": context,
            "question": question
        }):
            print(chunk, end='', flush=True)
        print()
    else:
        result = chain.invoke({
            "context": context,
            "question": question
        })
        print(result)