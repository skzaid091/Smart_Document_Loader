import re
import cv2
from ..ocr_processor import OCRProcessor


class FormulaImageExtractor:
    """
    Extract formula regions from rendered document pages.

    Responsibilities:
    - Crop detected formula regions
    - Save cropped formula images
    - Store crop paths for downstream formula recognition
    """

    def __init__(self, workspace, llm_service, ocr_config, text_element_types):
        """
        Initialize the formula image extractor.
        """

        self.workspace = workspace
        self.ocr_processor = OCRProcessor(llm_service, ocr_config, text_element_types)


    def save_crop_for_inspection(self, document_id, crop):
        """
        Save a cropped formula image.

        Persisting cropped formulas simplifies debugging
        and allows the recognition model to operate on
        individual formula images.
        """

        output_path = self.workspace.crop_path(document_id)

        cv2.imwrite(output_path, crop)

        return output_path


    def extract(self, document_id, element, page):
        """
        Extract a formula crop from a rendered page.

        The crop is saved to the document workspace and
        its path is returned for downstream recognition.
        """

        page_image = cv2.imread(page.image_path)

        if page_image is None:
            return None

        height, width = page_image.shape[:2]

        x1, y1, x2, y2 = map(int, element.bbox)

        # Clamp coordinates to remain within image boundaries.
        x1 = max(0, min(x1, width))
        x2 = max(0, min(x2, width))

        y1 = max(0, min(y1, height))
        y2 = max(0, min(y2, height))

        crop = page_image[y1:y2, x1:x2]

        # Ignore invalid or empty crops.
        if crop.size == 0:
            return None
        
        print("FFFFFFFFFFFFFORMULA CROP SIZE : ", crop.size)
    
        formula_text = self.ocr_processor._extract_text(crop)
        if not formula_text:
            print("Returned -----------------------------------------------------------------")
            return None
        
        formula_text = formula_text.strip().replace(" ", "").replace("\n", "")
        print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFF : ", formula_text)
        if re.fullmatch(r"\(?\d+\)?", formula_text):
            print("Returned -----------------------------------------------------------------")
            return None
        
        print("\n")

        crop_path = self.save_crop_for_inspection(document_id, crop)

        # Store the crop path for the formula recognition stage.
        element.metadata["formula_crop_path"] = crop_path

        return crop_path


    def process(self, document):
        """
        Extract cropped images for all detected formulas
        in the document.
        """

        document_id = document.document_id

        for element in document.elements:

            if element.element_type != "formula":
                continue

            page = document.get_page(element.page_number)

            crop_path = self.extract(document_id, element, page)

            # Store the cropped formula image for recognition.
            if crop_path:
                element.image_path = crop_path

        return document