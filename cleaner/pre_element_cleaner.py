class PreElementCleaner:
    """
    Clean extracted document elements.

    Responsibilities:
    - Remove empty text elements
    - Remove duplicate text elements
    - Preserve non-text elements
      (tables, figures, images, etc.)

    This stage reduces noise before chunking,
    indexing, and retrieval.
    """

    def __init__(self, text_element_types):

        self.text_element_types = text_element_types
        

    def process(self, document):
        """
        Clean document elements.

        Rules:
        1. Remove text elements with no content.
        2. Remove duplicate text elements on the
           same page.
        3. Keep all non-text elements unchanged.
        """

        cleaned = []

        # Tracks unique text content seen on
        # each page.
        seen = set()

        for element in document.elements:

            #
            # Only text elements participate
            # in deduplication.
            #
            if (element.element_type in self.text_element_types):

                # Remove empty text regions.
                if (not element.text or not element.text.strip()):
                    continue

                # Use normalized text content
                # for duplicate detection.
                key = (
                    element.page_number,
                    element.text
                    .strip()
                    .lower()
                )

                # Skip duplicate text blocks.
                if key in seen:
                    continue

                seen.add(key)

            # Keep valid elements.
            cleaned.append(element)

        document.elements = cleaned

        return document