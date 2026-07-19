from google import genai
from google.genai.types import GenerateContentConfig

from .base_llm import Base_LLM


class Gemini_LLM(Base_LLM):
    """
    Gemini Large Language Model interface.

    This class provides a unified interface for interacting with
    Google's Gemini language models.

    Parameters
    ----------
    model : str
        Gemini model name
        (e.g. ``models/gemini-3.5-flash``).

    api_key : str
        Google AI Studio API key.
    """

    def __init__(self, model: str, api_key: str):

        self.model = model

        self.client = genai.Client(
            api_key=api_key,
        )


    def invoke(self, prompt: str, system_prompt: str | None = None, temperature: float = 0.1, **kwargs) -> str:
        """
        Generate a response from a Gemini language model.

        Parameters
        ----------
        prompt : str
            User prompt.

        system_prompt : str, optional
            System instruction used to guide the model's behaviour.

        temperature : float, default=0.1
            Sampling temperature. Lower values produce more deterministic
            responses.

        **kwargs
            Additional keyword arguments forwarded to
            ``generate_content()``.

        Returns
        -------
        str
            Model-generated response.

        Raises
        ------
        RuntimeError
            If the Gemini inference request fails.
        """

        try:

            config = GenerateContentConfig(
                temperature=temperature,
                system_instruction=system_prompt,
                **kwargs,
            )

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )

        except Exception as e:
            raise RuntimeError(
                f"Gemini inference failed: {e}"
            ) from e

        return response.text