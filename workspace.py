from pathlib import Path
from uuid import uuid4
import shutil


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

    def __init__(self, base_dir, root_dir="temp"):
        """
        Initialize the workspace manager.

        Parameters
        ----------
        base_dir : Path
            Base directory of the project.

        root_dir : str
            Directory used for temporary processing files.
        """

        self.root_dir = Path(base_dir) / root_dir
        self.root_dir.mkdir(parents=True, exist_ok=True)


    def create(self, pdf_path):
        """
        Create a workspace for a document.

        A copy of the PDF is stored so the original file remains
        untouched during processing.

        Parameters
        ----------
        pdf_path : str | Path

        Returns
        -------
        tuple
            (document_id, workspace_pdf_path)
        """

        document_id = uuid4().hex

        workspace = self.root_dir / document_id

        workspace.mkdir(parents=True, exist_ok=True)

        (workspace / "rendered_pages").mkdir(exist_ok=True)
        (workspace / "element_crops").mkdir(exist_ok=True)

        destination = workspace / "document.pdf"

        shutil.copy2(pdf_path, destination)

        return document_id, destination


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