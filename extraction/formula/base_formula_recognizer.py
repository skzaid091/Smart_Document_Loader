import re
import json
from PIL import Image
from pathlib import Path
from json_repair import repair_json

class BaseFormulaRecognizer:

    def read_image(self, image):
        """
        Load an image from disk.

        Parameters
        ----------
        image : str | Path | PIL.Image.Image
            Image path or an already loaded PIL image.

        Returns
        -------
        PIL.Image.Image
            RGB image ready for inference.
        """

        if isinstance(image, Image.Image):
            return image.convert("RGB")

        if isinstance(image, (str, Path)):
            image = Path(image)

            if not image.exists():
                raise FileNotFoundError(
                    f"Image not found: {image}"
                )

            return Image.open(image).convert("RGB")

        raise TypeError("Image must be a file path or PIL.Image.Image.")


    def extract_json(self, response):

        if not response:
            raise ValueError("Empty response received.")

        response = response.strip()

        match = re.search(r"\{[\s\S]*\}", response)

        if not match:
            raise ValueError(f"No JSON found:\n{response}")

        return json.loads(repair_json(match.group()))
    
    
    def recognize(self, image_path):
        raise NotImplementedError