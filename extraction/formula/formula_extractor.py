from .formula_image_extractor import FormulaImageExtractor
from .vlm_formula_recognizer import VLMFormulaRecognizer


class FormulaExtractor:
    """
    Extract mathematical formulas from document pages.

    Responsibilities:
    - Crop detected formula regions
    - Recognize formulas using Pix2Tex
    - Store the recognized LaTeX representation
    """

    def __init__(self, workspace, llm_service, vlm_service, formula_elements, ocr_config, text_element_types):
        """
        Initialize the formula extraction pipeline.
        """

        self.formula_elements = formula_elements

        self.formula_image_extractor = FormulaImageExtractor(workspace, llm_service, ocr_config, text_element_types)
        self.vlm_based_formula_recognizer = VLMFormulaRecognizer(vlm_service)


    def process(self, document):
        """
        Extract and recognize all formulas present in the document.

        Formula regions are first cropped from rendered pages and
        then passed to the recognition model to generate LaTeX
        representations.
        """

        # Extract cropped images for all detected formulas.
        document = self.formula_image_extractor.process(document)

        for element in document.elements:

            if element.element_type not in self.formula_elements or not element.image_path:
                continue

            element.formula_data = self.vlm_based_formula_recognizer.recognize(element.image_path)

        return document