from .ocr_processor import OCRProcessor
from .pdf_processor import PDFTextExtractor


class TextExtractor:
    """
    Extracts textual content from documents.

    This component acts as a router between:

    - Native PDF text extraction
    - OCR-based text extraction

    Selection is performed on a page-by-page basis
    depending on whether a text layer is available.
    """

    def __init__(self, llm_service, ocr_config, text_element_types, generate_element_description):
        """
        Initialize text extraction components.
        """

        # Used for scanned documents and images.
        self.ocr_processor = OCRProcessor(llm_service, ocr_config, text_element_types)

        # Used for searchable PDFs containing
        # an embedded text layer.
        self.pdf_text_extractor = PDFTextExtractor(llm_service, text_element_types, generate_element_description)


    def process(self, document):
        """
        Extract text from all document pages.

        Workflow:
        1. Skip document types that do not contain
           page-based text content.
        2. Use native PDF text extraction whenever
           a text layer exists.
        3. Fall back to OCR otherwise.
        """

        for page in document.pages:

            # Native PDF text extraction provides
            # higher accuracy and better structure
            # preservation than OCR.
            if page.has_text_layer:
                self.pdf_text_extractor.process_page(document, page)

            # Use OCR for scanned PDFs and images.
            else:
                self.ocr_processor.process_page(document, page)

        return document