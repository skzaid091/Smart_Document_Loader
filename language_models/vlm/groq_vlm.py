from pathlib import Path

from groq import Groq

from .base_vlm import Base_VLM
from .utils import get_url


class Groq_VLM(Base_VLM):
    """
    Groq Vision-Language Model interface.

    This class provides a unified interface for performing multimodal
    inference using Groq-hosted vision-language models.

    Images are converted to a data URL before being sent to the Groq API.

    Parameters
    ----------
    model : str
        Groq vision-language model name.

    api_key : str
        Groq API key.
    """

    def __init__(self, model: str, api_key: str):

        self.model = model
        self.client = Groq(api_key=api_key)


    def invoke(self, image_path, prompt: str, **kwargs) -> str:
        """
        Perform multimodal inference using a Groq VLM.

        Parameters
        ----------
        image_path : str | Path
            Path to the input image.

        prompt : str
            Prompt describing the required task.

        **kwargs
            Additional keyword arguments forwarded to
            ``chat.completions.create()``.

        Returns
        -------
        str
            Generated response from the model.

        Raises
        ------

        RuntimeError
            If the Groq inference request fails.
        """

        image_path = Path(image_path)

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                messages=[
                    {
                        "role": "user",
                        "content": [

                            {
                                "type": "text",
                                "text": prompt,
                            },

                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": get_url(image_path),
                                },
                            },
                        ],
                    }
                ],

                **kwargs,
            )

        except Exception as e:
            raise RuntimeError(
                f"Groq inference failed: {e}"
            ) from e

        return response.choices[0].message.content