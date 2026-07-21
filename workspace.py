import os
import shutil
from uuid import uuid4
from pathlib import Path


class Workspace:
    """
    Manages temporary files generated during document processing.

    Workspace Structure
    -------------------
    temp/
    └── <document_id>/
        ├── document.pdf
        ├── rendered_pages/
        │   ├── page_1.png
        │   └── ...
        └── element_crops/
            ├── xxxx.png
            └── ...
    """

    def __init__(self, base_dir, raw_documents_dir, root_dir="temp"):
        """
        Initialize the workspace manager.

        Parameters
        ----------
        base_dir : str or Path
            Base directory used to store temporary processing workspaces.

        raw_documents_dir : str or Path
            Directory where copies of the original source documents are
            stored. Relative paths are resolved against the current working
            directory, while absolute paths are used as-is.

        root_dir : str
            Name of the directory created under `base_dir` for temporary
            processing workspaces.
        """

        # Create the root directory used to store temporary workspaces.
        self.root_dir = Path(base_dir) / root_dir
        self.root_dir.mkdir(parents=True, exist_ok=True)

        self.raw_documents_dir = Path(raw_documents_dir)
        
        # Resolve relative paths against the current working directory.
        if not self.raw_documents_dir.is_absolute():
            self.raw_documents_dir = Path.cwd() / self.raw_documents_dir

        # Convert to a canonical absolute path and create the directory.
        self.raw_documents_dir = self.raw_documents_dir.resolve()
        self.raw_documents_dir.mkdir(parents=True, exist_ok=True)
    

    def save_document(self, path):
        """
        Save a copy of the source document to the configured documents directory.

        Parameters
        ----------
        path : str or Path
            Path to the source document.

        Returns
        -------
        Path
            Absolute path to the copied document.
        """
        path = Path(path)

        destination = self.raw_documents_dir / path.name

        shutil.copy2(path, destination)

        return destination


    def create(self):
        """
        Create a temporary workspace for processing a document.

        A unique workspace is created for the document along with the
        required subdirectories used during the document processing
        pipeline.

        Returns
        -------
        str
            Unique identifier of the created workspace.
        """

        document_id = str(uuid4()).split('-')[-1]

        workspace = self.root_dir / document_id

        workspace.mkdir(parents=True, exist_ok=True)

        (workspace / "rendered_pages").mkdir(exist_ok=True)
        (workspace / "element_crops").mkdir(exist_ok=True)

        return document_id


    def page_path(self, document_id, page_number):
        """
        Return the output path for a rendered page image.
        """

        return (
            self.root_dir
            / document_id
            / "rendered_pages"
            / f"page_{page_number}.png"
        )


    def crop_path(self, document_id):
        """
        Generate a unique file path for a cropped document element.
        """

        return (
            self.root_dir
            / document_id
            / "element_crops"
            / f"{uuid4().hex}.png"
        )


    def cleanup(self, document_id):
        """
        Delete the workspace and all temporary files associated
        with a document.
        """

        workspace = self.root_dir / document_id

        if workspace.exists():
            shutil.rmtree(workspace)