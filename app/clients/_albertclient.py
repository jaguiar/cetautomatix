from openai import OpenAI
import requests
from io import BytesIO
from httpx import AsyncClient, Response
from app.config.settings import AlbertApiSettings
from ._genericasynhttpclient import GenericAsyncHttpClient, BearerAuth
from app.config.logging import logger

class AlbertClient(GenericAsyncHttpClient):
    def __init__(self, settings: AlbertApiSettings, httpx_client: AsyncClient):
        GenericAsyncHttpClient.__init__(self, base_url=settings.base_url, auth=BearerAuth(api_key=settings.api_key.get_secret_value()), httpx_client=httpx_client)
        self.openAI_client = OpenAI(base_url=self.base_url, api_key=settings.api_key.get_secret_value())
        self.httpx_client = httpx_client
        self.language_model = settings.language_model

    async def fetch_available_models(self) -> dict:
        """ Call the GET /models endpoint of the Albert API to get available models """
        response = await GenericAsyncHttpClient.get(self,"/models", timeout=None )
        data = response.json()
        models = {v["id"]: v for v in data["data"] if v["type"] == "text-generation"}
        return models

    async def fetch_collections(self) -> dict:
        """Call the GET /collections endpoint of the Albert API"""
        logger.debug("fetching collections")
        response = await GenericAsyncHttpClient.get(self,"/collections", timeout=None ) ## FIXME sometimes we need a very long timeout, need to check this point
        logger.debug("fetching collections done")
        data = response.json()
        collections_by_id = {v["id"]: v for v in data["data"]}
        return collections_by_id

    async def ask_for_document_summary(self, document_url: str, collections_to_use: list[str]) -> dict:
        """
            Use AlbertAPI to ask for a summary of a document
            We should be able to somehow specify which collections to use when it will be functional 
        """
        logger.debug(f"Ask for document summary with document url: {document_url}")
        doc_summary_user_message=f"""Salut Albert, je suis Cétautomatix, j'aimerais que tu me résumes le document suivant: {document_url}"""
        messages = [{"role": "user", "content": f"{doc_summary_user_message}"}]
        logger.debug(f" and messages: {messages}")
        answer = await self.ask(messages=messages, collections=collections_to_use)
        logger.debug(f"End asking, answer: {answer}")
        return answer
    
    #### utils methods
    async def ask(self, messages: list[dict], collections: list[str], **other_params) -> str:
        """ 
        Call the POST /chat/completions endpoint of the Albert API to chat with Albert 
        see collab: https://colab.research.google.com/github/etalab-ia/albert-api/blob/main/docs/tutorials/retrieval_augmented_generation.ipynb#scrollTo=e2e1368a
        """
        response = await GenericAsyncHttpClient.post(
            self, 
            "/chat/completions", 
             json={
                "messages": messages,
                "model": self.language_model,
                "stream": False,
                "n": 1,
                "search": True,
                "search_args": {"collections": [], "k": 6, "method": "semantic"}
        }) 
        answer = response.json().choices[0].message.content
        return answer

    def ask2(self, messages: list[dict], collections: list[str], **other_params) -> str:
        """ 
            Same than the previous one but with openAI client, so you have to be sync and you can't use the search part ?!
            see collab: https://colab.research.google.com/github/etalab-ia/albert-api/blob/main/docs/tutorials/chat_completions.ipynb#scrollTo=3f700cab-e53f-4a4c-8cbc-be9bdf96a7d7
        """
        result = self.openAI_client.chat.completions.create(
            model=self.language_model, 
            messages=messages,
            **other_params
        )
        answer = result.choices[0].message.content
        return answer
