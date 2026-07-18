from .ocr_correction.ocr_text_correction import TextLLMCorrector
from ..data_models import DocumentElement

class PDFTextExtractor:
    """
    Extracts text for layout elements from PDFs that
    already contain a searchable text layer.

    Workflow:
    1. Convert PDF text block coordinates into
       rendered-image coordinates.
    2. Match text blocks to detected layout elements.
    3. Aggregate matching text.
    4. Populate DocumentElement.text.
    """

    def __init__(self, llm_service, text_element_types):
        """
        Store application configuration.
        """
        self.text_llm_corrector = TextLLMCorrector(llm_service)

        self.text_element_types = text_element_types


    def _overlap_ratio(self, element_bbox, block_bbox):
        """
        Compute how much of a text block is covered
        by a detected layout element.

        Returns:
            intersection_area / block_area

        Using block coverage rather than IoU helps
        determine whether a text block belongs to a
        particular layout region.
        """

        x_left = max(element_bbox[0], block_bbox[0])
        y_top = max(element_bbox[1], block_bbox[1])

        x_right = min(element_bbox[2], block_bbox[2])
        y_bottom = min(element_bbox[3], block_bbox[3])

        if (x_right <= x_left or y_bottom <= y_top):
            return 0.0

        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        block_area = (block_bbox[2] - block_bbox[0]) * (block_bbox[3] - block_bbox[1])

        if block_area <= 0:
            return 0.0

        return (
            intersection_area
            / block_area
        )


    def _scale_bbox(self, pdf_bbox, page):
        """
        Convert PDF coordinates into rendered-image
        coordinates.

        Layout detection operates on rendered page
        images, therefore PDF text blocks must be
        mapped into the same coordinate system.
        """

        scale_x = page.rendered_width / page.original_width
        scale_y = page.rendered_height / page.original_height

        return [
            pdf_bbox[0] * scale_x,
            pdf_bbox[1] * scale_y,
            pdf_bbox[2] * scale_x,
            pdf_bbox[3] * scale_y,
        ]


    def _assign_text_blocks(self, page, page_elements):
        """
        Assign every PyMuPDF text block to the layout element
        with the highest overlap.

        Returns
        -------
        tuple
            (
                assignments,
                unmatched_blocks
            )

        assignments:
            {
                element_index: [
                    {
                        "bbox": [...],
                        "text": "...",
                        "y": ...
                    },
                    ...
                ]
            }

        unmatched_blocks:
            [
                {
                    "bbox": [...],
                    "text": "...",
                    "y": ...
                }
            ]
        """

        MIN_OVERLAP = 0.10

        assignments = {
            idx: []
            for idx, element in enumerate(page_elements)
            if element.element_type in self.text_element_types
        }

        unmatched_blocks = []

        for block in page.text_blocks:

            scaled_bbox = self._scale_bbox(
                block["bbox"],
                page
            )

            best_overlap = 0.0
            best_element_idx = None

            for idx, element in enumerate(page_elements):

                if element.element_type not in self.text_element_types:
                    continue

                overlap = self._overlap_ratio(
                    element.bbox,
                    scaled_bbox,
                )

                if overlap > best_overlap:
                    best_overlap = overlap
                    best_element_idx = idx

            block_data = {
                "bbox": scaled_bbox,
                "text": block["text"],
                "y": scaled_bbox[1],
            }

            if (best_element_idx is not None and best_overlap >= MIN_OVERLAP):
                assignments[best_element_idx].append(block_data)

            else:
                unmatched_blocks.append(block_data)

        return assignments, unmatched_blocks


    def process_page(self, document, page):

        page_elements = [
            element
            for element in document.elements
            if element.page_number == page.page_number
        ]

        assignments, unmatched_blocks = self._assign_text_blocks(
            page,
            page_elements,
        )

        for idx, element in enumerate(page_elements):

            if element.element_type not in self.text_element_types:
                continue

            matched_blocks = assignments[idx]

            matched_blocks.sort(
                key=lambda block: block["y"]
            )

            element.text = "\n".join(
                block["text"]
                for block in matched_blocks
            )

        for block in unmatched_blocks:

            document.elements.append(
                DocumentElement(
                    page_number=page.page_number,
                    element_type="plain text",
                    confidence=1.0,
                    bbox=block["bbox"],
                    text=block["text"],
                    metadata={}
                )
            )

        return document