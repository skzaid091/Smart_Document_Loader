from .groq_vlm import Groq_VLM
from .huggingface_vlm import HuggingFace_VLM
from .gemini_vlm import Gemini_VLM


class VLM_Service:

    @staticmethod
    def create(vlm_config, vlm_models):

        provider = vlm_config["provider"].lower()
        api_key = vlm_config["api_key"]

        if provider == "groq":

            return Groq_VLM(
                model=vlm_models["groq"]["model"],
                api_key=api_key
            )

        elif provider == "huggingface":

            return HuggingFace_VLM(
                model=vlm_models["huggingface"]["model"],
                api_key=api_key, 
                provider=vlm_models["huggingface"]["provider"],
            )

        elif provider == "gemini":

            return Gemini_VLM(
                model=vlm_models["gemini"]["model"], 
                api_key=api_key
            )

        raise ValueError(
            f"Unsupported VLM provider: {provider}"
        )