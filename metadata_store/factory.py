"""
Metadata store factory.
"""

from .base import BaseMetadataStore
from .mongodb import MongoDBMetadataStore


class MetadataStoreFactory:
    """
    Factory for creating metadata store instances.
    """

    @staticmethod
    def create(root_dir, config) -> BaseMetadataStore:
        """
        Create a metadata store.

        Parameters
        ----------
        config
            Metadata store configuration.

        Returns
        -------
        BaseMetadataStore
            Metadata store instance.

        Raises
        ------
        ValueError
            If the metadata store type is unsupported.
        """

        metadata_store_type = config["type"].lower()

        if metadata_store_type == "mongodb":

            return MongoDBMetadataStore(
                uri=config["uri"],
                database=config["database"],
                collection=config["collection"],
            )

        raise ValueError(
            f"Unsupported metadata store: "
            f"{metadata_store_type}"
        )