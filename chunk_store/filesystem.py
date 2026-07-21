"""
Filesystem chunk store.
"""

from pathlib import Path
from typing import List

from langchain_core.documents import Document

from .base import BaseChunkStore
from .document_serializer import DocumentSerializer


class FilesystemChunkStore(BaseChunkStore):
    """
    Store processed chunks on the local filesystem.
    """

    def __init__(self, root_dir, output_directory: str | Path) -> None:
        """
        Initialize the chunk store.

        Parameters
        ----------
        output_directory : str | Path
            Directory where processed documents are stored.
        """

        self.save_directory = Path(root_dir) / Path(output_directory)

        self.save_directory.mkdir(
            parents=True,
            exist_ok=True,
        )


    def save(self, document_id: str, document_chunks: List[Document]) -> Path:
        """
        Save processed document chunks.
        """

        document_directory = (
            self.save_directory /
            document_id
        )

        document_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        chunk_path = (
            document_directory /
            "chunks.sdl"
        )

        DocumentSerializer.save(
            document_chunks,
            chunk_path,
        )

        return chunk_path