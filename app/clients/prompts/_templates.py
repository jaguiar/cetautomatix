from abc import ABC, abstractmethod
from typing import Optional, List, Dict

### It seems that langchain has something similar, but hadn't time to dig into it


class PromptTemplate(ABC):
    @abstractmethod
    def as_prompt(self, **kwargs) -> List[Dict[str, str]]:
        """
        Return a prompt with the given constructor arguments
        """
        pass


class DocumentSummaryUserMessage(PromptTemplate):
    def __init__(self, document_url: str, topic_of_interest: Optional[str] = None):
        topic_of_interest_part = (
            ""
            if topic_of_interest is None
            else f"""
                    d'une manière générale, puis que tu détailles plus particulièrement ce qui concerne le sujet '{topic_of_interest}'
                """
        )

        self.prompt_message = f"""
            Salut Albert, je suis Cétautomatix, j'aimerais que tu me résumes le document suivant:
            {document_url} {topic_of_interest_part}
        """

    def as_prompt(self, **kwargs) -> List[Dict[str, str]]:
        return [{"role": "user", "content": self.prompt_message}]
