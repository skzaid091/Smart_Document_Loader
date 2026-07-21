from abc import ABC, abstractmethod

from ..data_models import DocumentMetadata


class BaseMetadataStore(ABC):
    """
    Base interface for persisting document metadata.
    """

    @abstractmethod
    def connect(self) -> None:
        """
        Establish a connection to the metadata store.
        """
        ...

    @abstractmethod
    def save(self, metadata: DocumentMetadata) -> None:
        """
        Persist document metadata.
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """
        Close the metadata store connection and release resources.
        """
        ...