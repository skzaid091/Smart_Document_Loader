from pathlib import Path

from PIL import Image
from pix2tex.cli import LatexOCR


class FormulaRecognizer:
    """
    Wrapper around Pix2Tex for mathematical formula recognition.
    """

    def __init__(self):

        self.model = LatexOCR()


    def recognize(self, image):
        """
        Convert a cropped formula image into LaTeX.

        Parameters
        ----------
        image : str | Path | PIL.Image.Image

        Returns
        -------
        str
            Predicted LaTeX expression.
        """

        if isinstance(image, (str, Path)):
            image = Image.open(image).convert("RGB")

        return self.model(image)