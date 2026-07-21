"""
MongoDB metadata store.
"""

from dataclasses import asdict

from .base import BaseMetadataStore
from ..data_models import DocumentMetadata


class MongoDBMetadataStore(BaseMetadataStore):
    """
    MongoDB implementation of the metadata store.
    """

    def __init__(self, uri: str, database: str, collection: str) -> None:
        """
        Initialize the MongoDB metadata store.

        Parameters
        ----------
        uri : str
            MongoDB connection URI.

        database : str
            MongoDB database name.

        collection : str
            MongoDB collection name.
        """

        self.uri = uri
        self.database = database
        self.collection_name = collection

        self.client = None
        self.collection = None

        self.connect()


    def connect(self) -> None:
        """
        Establish a connection to MongoDB.
        """
        
        try:
            from pymongo import MongoClient
        except ImportError as exc:
            raise ImportError(
                "MongoDB support requires the 'pymongo' package.\n"
                "Install it using:\n\n"
                "    pip install pymongo"
            ) from exc
        
        self.client = MongoClient(self.uri)

        self.collection = self.client[
            self.database
        ][
            self.collection_name
        ]


    def save(self, metadata: DocumentMetadata) -> None:
        """
        Persist document metadata.

        Parameters
        ----------
        metadata : DocumentMetadata
            Document metadata to store.
        """

        self.collection.insert_one(
            self._serialize(metadata)
        )


    def close(self) -> None:
        """
        Close the MongoDB connection.
        """

        if self.client is not None:
            self.client.close()


    # ------------------------------------------------------------------
    # Helper Methods
    # ------------------------------------------------------------------

    @staticmethod
    def _serialize(metadata: DocumentMetadata) -> dict:
        """
        Convert a DocumentMetadata instance into a MongoDB document.

        Parameters
        ----------
        metadata : DocumentMetadata
            Metadata object.

        Returns
        -------
        dict
            MongoDB-compatible document.
        """

        document = asdict(metadata)

        if metadata.source_path is not None:
            document["source_path"] = str(
                metadata.source_path
            )

        return document