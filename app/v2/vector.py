from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import pandas as pd
import os

from document_manager import DocumentManager

embeddings = OllamaEmbeddings(model="nomic-embed-text")

db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

vector_store = Chroma(
    collection_name="choreo_knowledge_base",
    embedding_function=embeddings,
    persist_directory=db_location
)

if add_documents:
    # If the database does not exist, we will add documents to it
    document_manager = DocumentManager(directory_path="./markdown_folder", glob_pattern="./*.md")
    document_manager.load_documents()
    document_manager.split_documents(split_level=3)
    all_sections = document_manager.get_all_sections()
    print(f"Number of sections to add: {len(all_sections)}")
    vector_store.add_documents(all_sections)

    # documents = []
    # ids = []
    # Logic to convert data to documents

retriever = vector_store.as_retriever(search_kwargs={"k": 5})

def inspect_vector_db(test_query="test query"):
    # Check number of documents in the vector store
    try:
        num_docs = vector_store._collection.count()
        print(f"Number of documents in vector DB: {num_docs}")
    except Exception as e:
        print(f"Error checking document count: {e}")

    # Try retrieving with a sample query
    try:
        results = retriever.invoke(test_query)
        print(f"Retriever returned {len(results)} results.")
        for i, doc in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"Content: {doc.page_content}")  # Print first 200 chars
            print(f"Metadata: {doc.metadata}")
    except Exception as e:
        print(f"Error testing retriever: {e}")

if __name__ == "__main__":
    inspect_vector_db('resource hierarchy')