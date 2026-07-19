from pathlib import Path

from PIL import Image, UnidentifiedImageError
from google import genai

from .base_vlm import Base_VLM


class Gemini_VLM(Base_VLM):
    """
    Gemini Vision-Language Model interface.

    This class provides a unified interface for performing multimodal
    inference using Google's Gemini models. It accepts an image and a
    textual prompt, then returns the model's generated response.

    Parameters
    ----------
    model : str
        Gemini model name (e.g. ``models/gemini-3.5-flash``).

    api_key : str
        Google AI Studio API key.
    """

    def __init__(self, model: str, api_key: str):

        self.model = model

        self.client = genai.Client(
            api_key=api_key
        )


    def invoke(self, image_path, prompt: str, **kwargs) -> str:
        """
        Perform multimodal inference using Gemini.

        Parameters
        ----------
        image_path : str | Path
            Path to the input image.

        prompt : str
            Text prompt describing the required task.

        **kwargs
            Additional keyword arguments forwarded to
            ``generate_content()``.

        Returns
        -------
        str
            Generated response from the Gemini model.

        Raises
        ------

        ValueError
            If the image cannot be opened.

        RuntimeError
            If Gemini inference fails.
        """

        image_path = Path(image_path)
        try:
            image = Image.open(image_path)

        except UnidentifiedImageError as e:
            raise ValueError(
                f"Unsupported or corrupted image: {image_path}"
            ) from e

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    image,
                    prompt,
                ],
                **kwargs,
            )

        except Exception as e:
            raise RuntimeError(
                f"Gemini inference failed: {e}"
            ) from e

        return response.text