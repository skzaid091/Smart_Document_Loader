from groq import Groq

from .base_llm import Base_LLM


class Groq_LLM(Base_LLM):
    """
    Groq Large Language Model interface.

    This class provides a unified interface for interacting with
    Groq-hosted language models.

    Parameters
    ----------
    model : str
        Groq model name.

    api_key : str
        Groq API key.
    """

    def __init__(self, model: str, api_key: str):

        self.model = model

        self.client = Groq(
            api_key=api_key,
        )


    def invoke(self, prompt: str, system_prompt: str | None = None, temperature: float = 0.1, **kwargs) -> str:
        """
        Generate a response from a Groq language model.

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
            ``chat.completions.create()``.

        Returns
        -------
        str
            Model-generated response.

        Raises
        ------
        RuntimeError
            If the Groq inference request fails.
        """

        messages = []

        if system_prompt:

            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        try:

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                **kwargs,
            )

        except Exception as e:
            raise RuntimeError(
                f"Groq inference failed: {e}"
            ) from e

        return response.choices[0].message.content