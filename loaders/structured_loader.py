from pathlib import Path

from langchain_community.document_loaders import (
    CSVLoader,
    JSONLoader,
    UnstructuredExcelLoader,
    UnstructuredXMLLoader
)

from .base_loader import BaseLoader


class StructuredLoader(BaseLoader):
    """
    Wrapper around LangChain loaders for structured documents.
    """

    def __init__(self, workspace):
        
        self.worksapce = workspace


    def load(self, path):

        path = self.worksapce.save_document(path)
        extension = path.suffix.lower()

        if extension == ".csv":
            loader = CSVLoader(file_path=str(path))

        elif extension in {".xls", ".xlsx", ".ods"}:
            loader = UnstructuredExcelLoader(str(path))

        elif extension in {".json", ".jsonl"}:
            loader = JSONLoader(file_path=str(path), jq_schema=".", text_content=False)

        elif extension == ".xml":
            loader = UnstructuredXMLLoader(str(path))

        else:
            raise ValueError(f"Unsupported structured document: {extension}")

        return path, loader.load()