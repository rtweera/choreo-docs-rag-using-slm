from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import pandas as pd
import os

embeddings = OllamaEmbeddings(model="nomic-embed-text")

db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

vector_store = Chroma(
    collection_name="choreo_knowledge_base",
    embedding_function=embeddings,
    persist_directory=db_location
)

if add_documents:
    documents = []
    ids = []
    # Logic to convert data to documents
    vector_store.add_documents(documents, ids=ids)
