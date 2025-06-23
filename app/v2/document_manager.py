from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
import os

class DocumentManager:
    def __init__(self, directory_path, glob_pattern="./*.md"):
        self.directory_path = directory_path
        self.glob_pattern = glob_pattern
        self.documents = []
        self.all_ids = []
        self.all_sections = []
    
    def load_documents(self):
        loader = DirectoryLoader(self.directory_path, glob=self.glob_pattern, show_progress=True, loader_cls=UnstructuredMarkdownLoader)
        self.documents = loader.load()

    def split_documents(self, split_level=2):
        """
        Splits the loaded documents into sections based on Markdown headers.

        Args:
            split_level (int, optional): Which heading level to split on. Defaults to 2.
        """
        headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3"), ("####", "Header 4")]
        text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on[:split_level])
        for doc in self.documents:
            sections = text_splitter.split_text(doc.page_content)
            self.all_sections.extend(sections)

    def get_all_sections(self):
        return self.all_sections