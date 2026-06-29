import os
import cv2
from uuid import uuid4


class TableImageExtractor:
    """
    Extract table regions from document pages.

    Responsibilities:
    - Locate table elements detected by the layout model
    - Crop table regions from rendered page images
    - Save crops for downstream processing
    - Store crop paths in element metadata

    These crops are later consumed by the table
    structure recognition pipeline.
    """

    def __init__(self, workspace):
        self.workspace = workspace


    def save_crop_for_inspection(self, document_id, crop):
        """
        Save a cropped table image.

        Storing crops on disk makes debugging and
        visual inspection significantly easier.
        """

        output_path = self.workspace.crop_path(document_id)
        
        cv2.imwrite(output_path, crop)

        return output_path


    def extract(self, document_id, element, page):
        """
        Extract the image region corresponding to a
        detected table element.

        The resulting crop is saved to disk and its
        path is stored in the element metadata.
        """

        page_image = cv2.imread(page.image_path)

        if page_image is None:
            return None

        height, width = page_image.shape[:2]

        x1, y1, x2, y2 = map(int, element.bbox)

        # Clamp bounding box coordinates to
        # image boundaries.
        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))

        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))

        crop = page_image[y1:y2, x1:x2]

        # Ignore invalid crops.
        if crop.size == 0:
            return None

        crop_path = self.save_crop_for_inspection(document_id, crop)

        # Store crop location for later stages
        # such as TATR and OCR.
        element.metadata["table_crop_path"] = crop_path

        return crop_path


    def process(self, document):
        """
        Extract crops for all detected tables in
        the document.
        """

        document_id = document.document_id

        table_crop_paths = []
        for element in document.elements:

            if element.element_type != "table":
                continue

            page = document.get_page(element.page_number)

            crop_path = self.extract(document_id, element, page)

            table_crop_paths.append(crop_path)


        return document