from .base_llm import Base_LLM


class OpenAI_LLM(Base_LLM):

    def __init__(self, *args, **kwargs):

        raise NotImplementedError(
            "OpenAI support coming soon."
        )


    def invoke(self, prompt: str, system_prompt: str | None = None, temperature: float = 0.1, **kwargs) -> str:

        raise NotImplementedError