from .table_image_extractor import TableImageExtractor
from .tatr_extractor import TATRExtractor
from ...extraction.ocr_processor import OCRProcessor
from .table_ocr import TableOCR
from .table_data_builder import TableDataBuilder

from ...extraction.ocr_correction.ocr_table_correction import TableLLMCorrector


class TableExtractor:
    """
    End-to-end table extraction pipeline.

    Workflow:

        Detected Table Region
                    ↓
          TableImageExtractor
                    ↓
            Cropped Table Image
                    ↓
             TATRExtractor
                    ↓
        Table Structure Detection
           (rows / columns / cells)
                    ↓
                TableOCR
                    ↓
          Cell Text Extraction
                    ↓
           TableDataBuilder
                    ↓
          Structured TableData
    """

    def __init__(self, workspace, llm_service, ocr_config, text_element_types, table_cell_padding):
        """
        Initialize all table-processing components.
        """
        self.enable_ocr_correction = ocr_config["enable_ocr_correction"]

        # Extract table regions from document pages.
        self.table_image_extractor = TableImageExtractor(workspace)

        # Detect table structure using
        # Microsoft's Table Transformer.
        self.tatr_extractor = TATRExtractor()

        # Perform OCR on detected table cells.
        self.table_ocr = TableOCR(table_cell_padding, OCRProcessor(llm_service, ocr_config, text_element_types))

        # Convert OCR results into a structured
        # TableData representation.
        self.table_data_builder = TableDataBuilder()

        self.table_llm_corrector = TableLLMCorrector(llm_service)


    def process(self, document):
        """
        Execute the complete table extraction pipeline.
        """

        # Crop detected table regions.
        document = self.table_image_extractor.process(document)

        # Detect rows, columns, and cells.
        document = self.tatr_extractor.process(document)

        # Extract text from table cells.
        document = self.table_ocr.process(document)

        # Build structured table data.
        document = self.table_data_builder.process(document)

        if self.enable_ocr_correction:
            document = self.table_llm_corrector.process(document)

        return document