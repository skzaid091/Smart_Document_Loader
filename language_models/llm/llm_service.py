from .groq_llm import Groq_LLM
from .huggingface_llm import HuggingFace_LLM
from .gemini_llm import Gemini_LLM
from .openai_llm import OpenAI_LLM


class LLM_Service:

    @staticmethod
    def create(llm_config, llm_models):

        provider = llm_config["provider"].lower()
        api_key = llm_config["api_key"]

        if provider == "groq":

            return Groq_LLM(
                model=llm_models["groq"]["model"],
                api_key=api_key
            )

        elif provider == "huggingface":

            return HuggingFace_LLM(
                model=llm_models["huggingface"]["model"],
                api_key=api_key, 
                provider=llm_models["huggingface"]["provider"]
            )

        elif provider == "gemini":

            return Gemini_LLM()

        elif provider == "openai":

            return OpenAI_LLM()

        raise ValueError(
            f"Unsupported LLM provider: {provider}"
        )