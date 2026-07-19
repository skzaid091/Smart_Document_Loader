from abc import ABC, abstractmethod


class Base_LLM(ABC):
    """
    Abstract interface for Large Language Models.
    """

    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """
        Generate a response from the language model.
        """
        pass