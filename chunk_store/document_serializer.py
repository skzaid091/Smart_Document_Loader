"""
Serializer for LangChain documents.
"""

import pickle
from pathlib import Path
from typing import List

from langchain_core.documents import Document


class DocumentSerializer:
    """
    Serialize document chunks.
    """

    @staticmethod
    def save(document_chunks: List[Document], path: Path) -> None:
        """
        Serialize document chunks.
        """

        data = [
            {
                "page_content": doc.page_content,
                "metadata": doc.metadata,
            }
            for doc in document_chunks
        ]

        with path.open("wb") as f:
            pickle.dump(data, f)