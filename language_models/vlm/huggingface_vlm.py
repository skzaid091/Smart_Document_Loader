from pathlib import Path

from huggingface_hub import InferenceClient

from .base_vlm import Base_VLM
from .utils import get_url


class HuggingFace_VLM(Base_VLM):
    """
    Hugging Face Vision-Language Model interface.

    This class provides a unified interface for performing multimodal
    inference using Hugging Face Inference Providers.

    Images are encoded as data URLs before being sent to the model.

    Parameters
    ----------
    model : str
        Hugging Face model name.

    api_key : str
        Hugging Face API key.

    provider : str
        Hugging Face inference provider
        (e.g. ``hf-inference``, ``together``, ``featherless-ai``).
    """

    def __init__(self, model: str, api_key: str, provider: str):

        self.model = model

        self.client = InferenceClient(
            provider=provider,
            api_key=api_key,
        )


    def invoke(self, image_path, prompt: str, **kwargs) -> str:
        """
        Perform multimodal inference using a Hugging Face VLM.

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
            If the Hugging Face inference request fails.
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
                f"Hugging Face inference failed: {e}"
            ) from e

        return response.choices[0].message.content