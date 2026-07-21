from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from langchain_core.documents import Document


class BaseChunkStore(ABC):
    """
    Base interface for storing processed document chunks.
    """

    @abstractmethod
    def save(self, document_id: str, documents: List[Document]) -> Path:
        """
        Persist processed document chunks.

        Returns
        -------
        Path
            Location where the chunks were stored.
        """
        ...