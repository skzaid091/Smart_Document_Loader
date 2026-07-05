class PostElementCleaner:
    """
    Perform generic cleanup on extracted document elements.

    Responsibilities:
    - Remove duplicate detections
    - Normalize extracted text
    - Prepare elements for downstream processing

    This stage operates only on the raw extraction output and
    performs document-agnostic cleanup before later semantic
    processing stages.

    Typical pipeline:

        Layout Detection
                ↓
              OCR
                ↓
        PostElementCleaner
                ↓
        Reading Order Reconstruction
                ↓
          Content Extraction
                ↓
            Data Cleaning
                ↓
          Section Building
                ↓
             Chunking
                ↓
             Retrieval
    """

    def _normalize_text(self, document):
        """
        Normalize OCR text.

        Operations:
        - Remove newlines
        - Remove tabs
        - Collapse repeated spaces

        Example:

            "Hello\\n\\nWorld"

        becomes:

            "Hello World"
        """

        for element in document.elements:

            # Some elements such as tables
            # and figures may not contain text.
            text = getattr(element, "text", None)

            if not text:
                continue

            text = str(text)

            # Replace newlines with spaces.
            text = text.replace("\n", " ")

            # Replace tab characters.
            text = text.replace("\t", " ")

            # Collapse repeated spaces.
            text = " ".join(text.split())

            element.text = text


    def iou(self, box1, box2):
        """
        Compute Intersection over Union (IoU)
        between two bounding boxes.

        Formula:

            IoU =
                Intersection Area
                -----------------
                    Union Area

        Returns:
            float in range [0, 1]

        Notes:
            0.0 -> No overlap
            1.0 -> Perfect overlap
        """

        # Handle invalid boxes.
        if not box1 or not box2:
            return 0.0

        # Compute overlap region.
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])

        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])

        # No overlap exists.
        if x2 <= x1 or y2 <= y1:
            return 0.0

        # Area of intersection.
        intersection = (x2 - x1) * (y2 - y1)

        # Area of first box.
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])

        # Area of second box.
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

        # Union area.
        union = area1 + area2 - intersection

        return intersection / union


    def process(self, document):
        """
        Clean extracted document elements.

        Workflow:

            Raw Elements
                ↓

        Duplicate Removal
                ↓

        Text Normalization
                ↓

        Clean Elements

        Steps:

            1. Remove duplicate detections using
            bounding-box overlap.

            2. Normalize extracted text by removing
            unnecessary whitespace while preserving
            the original content.

        Returns:
            Cleaned document with duplicate elements
            removed and text normalized.
        """

        filtered = []

        # ----------------------------------
        # Remove duplicate detections
        # ----------------------------------

        for element in document.elements:

            duplicate = False

            for existing in filtered:

                # Compare only elements
                # from the same page.
                if element.page_number != existing.page_number:
                    continue

                overlap = self.iou(element.bbox, existing.bbox)

                # Consider elements duplicates
                # if overlap exceeds threshold.
                if overlap > 0.7:

                    # Prefer element containing
                    # more extracted text.
                    current_len = len(getattr(element, "text", "") or "")
                    existing_len = len(getattr(existing, "text", "" ) or "")

                    if current_len > existing_len:
                        filtered.remove(existing)
                        filtered.append(element)

                    duplicate = True

                    break

            if not duplicate:
                filtered.append(element)

        document.elements = filtered

        # ----------------------------------
        # Normalize extracted text
        # ----------------------------------

        self._normalize_text(document)

        return document