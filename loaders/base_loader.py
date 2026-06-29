class BaseLoader:
    """Base interface for all document loaders."""

    def load(self, path):
        # Load the document and return a Document object.
        raise NotImplementedError