import os
from PIL import Image

from ..data_models import *
from ..workspace import Workspace

from .base_loader import BaseLoader


class ImageLoader(BaseLoader):

    def __init__(self, workspace):
        self.workspace = workspace


    def load(self, path):
        """
        Load an image file and return it as a single-page Document.
        """

        file_name = os.path.basename(path)
        document_id, path = self.workspace.create(path)

        try:
            # Read image metadata.
            with Image.open(path) as image:

                width, height = image.size

                metadata = {
                    "format": image.format,
                    "mode": image.mode,
                    "file_path": path
                }

            # Represent the image as a single document page.
            page = PageContent(
                page_number=1,
                has_text_layer=False,

                text_blocks=[],

                original_width=width,
                original_height=height,

                image_path=path
            )

            return Document(
                document_id=document_id,
                document_type="image",

                file_name=file_name,
                metadata=metadata,

                page_count=1,
                pages=[page],

                error=None
            )

        except Exception as e:

            # Return a valid Document containing error details.
            return Document(
                document_id=document_id,
                document_type="image",

                file_name=file_name,
                metadata={},

                page_count=0,
                pages=[],

                error=f"Failed to load image: {e}"
            )