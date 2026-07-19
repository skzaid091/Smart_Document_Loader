from abc import ABC, abstractmethod


class Base_VLM(ABC):
    """
    Abstract interface for Vision-Language Models.
    """

    @abstractmethod
    def invoke(self, image_path: str, prompt: str) -> str:
        """
        Send an image and prompt to the VLM.

        Returns
        -------
        str
            Generated response.
        """
        pass