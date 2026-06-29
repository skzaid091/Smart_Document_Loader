from pathlib import Path

from langchain_community.document_loaders import (
    TextLoader as LangChainTextLoader,
    BSHTMLLoader,
    UnstructuredMarkdownLoader
)

from .base_loader import BaseLoader


class TextLoader(BaseLoader):
    """
    Wrapper around LangChain loaders for plain text documents.
    """

    def load(self, path):

        path = Path(path)
        extension = path.suffix.lower()

        if extension == ".txt":
            loader = LangChainTextLoader(str(path), encoding="utf-8")

        elif extension == ".md":
            loader = UnstructuredMarkdownLoader(str(path))

        elif extension == ".html":
            loader = BSHTMLLoader(str(path))

        else:
            raise ValueError(f"Unsupported text document: {extension}")

        return loader.load()