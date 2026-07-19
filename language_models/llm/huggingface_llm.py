from huggingface_hub import InferenceClient

from .base_llm import Base_LLM


class HuggingFace_LLM(Base_LLM):
    """
    Hugging Face Large Language Model interface.

    This class provides a unified interface for interacting with
    Hugging Face hosted language models through the Inference API.

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


    def invoke(self, prompt: str, system_prompt: str | None = None, temperature: float = 0.1, **kwargs) -> str:
        """
        Generate a response from a Hugging Face language model.

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
            If the Hugging Face inference request fails.
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
                f"Hugging Face inference failed: {e}"
            ) from e

        return response.choices[0].message.content