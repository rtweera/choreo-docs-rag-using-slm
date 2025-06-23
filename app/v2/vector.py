from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import pandas as pd
import os

from document_manager import DocumentManager

full_mode = False  # Set to True to use the full Choreo knowledge base, False for the Choreo concepts database
forced_overwrite = False  # Set to True to force overwrite the existing database


choreo_concepts_db_location = "./chroma_choreo_concepts_db"
all_choreo_db_location = "./chroma_all_choreo_db"
choreo_concepts_markdown_folder = "./choreo_concepts_markdown_folder"
all_choreo_markdown_folder = "./all_choreo_markdown_folder"

if full_mode and not os.path.exists(all_choreo_markdown_folder):
    raise FileNotFoundError(f"Full mode is enabled, but the folder '{all_choreo_markdown_folder}' does not exist. Wrong path or missing data?")
elif not full_mode and not os.path.exists(choreo_concepts_markdown_folder):
    raise FileNotFoundError(f"Full mode is disabled, but the folder '{choreo_concepts_markdown_folder}' does not exist. Wrong path or missing data?")

embeddings = OllamaEmbeddings(model="nomic-embed-text")

db_location = all_choreo_db_location if full_mode else choreo_concepts_db_location
markdown_folder = all_choreo_markdown_folder if full_mode else choreo_concepts_markdown_folder
add_documents = not os.path.exists(db_location)

vector_store = Chroma(
    collection_name="choreo_knowledge_base",
    embedding_function=embeddings,
    persist_directory=db_location
)

if add_documents or forced_overwrite:
    # If the database does not exist, we will add documents to it
    document_manager = DocumentManager(directory_path=markdown_folder, glob_pattern="**/*.md")
    document_manager.load_documents()
    document_manager.split_documents(split_level=3)
    all_sections = document_manager.get_all_sections()
    print(f"Number of sections to add: {len(all_sections)}")
    vector_store.add_documents(all_sections)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})
print("Vectorising part is done.")

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