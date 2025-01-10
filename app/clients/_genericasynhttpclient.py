from abc import ABC, abstractmethod
from io import BytesIO
from httpx import AsyncClient, Response, Auth, Limits, Timeout
from app.config.settings import Settings, HttpxSettings
from app.config.logging import logger 
from typing import Optional

class GenericAsyncHttpClient(ABC):
    def __init__(self, base_url: str, httpx_client: AsyncClient, auth: Optional[Auth] = None, default_headers: Optional[dict] = None):
        self.base_url = base_url
        self.httpx_client = httpx_client
        self.auth = auth
        self.default_headers = default_headers if default_headers is not None else {} #clean?!
        #self.httpx_client.auth = auth
        logger.info(f"GenericAsyncHttpClient initialized for {base_url}")

    async def close(self):
        self.httpx_client.aclose()
  
    def generate(self, model: str, messages: list[dict], **sampling_params) -> str:
        result = self.openAIClient.chat.completions.create(
            model=model, messages=messages, **sampling_params
        )
        answer = result.choices[0].message.content
        return answer

    async def get(self, url_path: str, **kwargs) -> Response:
        # headers should be merged with default headers on client hopefully : https://www.python-httpx.org/advanced/clients/#merging-of-configuration
        headers = {**self.default_headers, **kwargs.get("headers", {})}
        return await self.httpx_client.get(
            # FIXME we should probably check or clean the url (looking for double "/" for example)
            f'{self.base_url}{url_path}', 
            auth=self.auth, 
            headers=headers,
            **kwargs
        )
    
    async def post(self, url_path: str, **kwargs) -> Response:
        # headers should be merged with default headers on client hopefully : https://www.python-httpx.org/advanced/clients/#merging-of-configuration
        headers = {**self.default_headers, **kwargs.get("headers", {})}
        return await self.httpx_client.post(
            # FIXME we should probably check or clean the url (looking for double "/" for example)
            f'{self.base_url}{url_path}', 
            auth=self.auth, 
            headers=headers,
            **kwargs
        )
        
     ### utils methods for logging - should it be in a separate file?
    @staticmethod
    async def raise_on_4xx_5xx(response: Response):
        response.raise_for_status()

    @staticmethod
    async def log_request(request):
        logger.info(f"Request event: {request.method} {request.url} {request.headers} - Waiting for response")

    @staticmethod
    async def log_response(response: Response):
        request = response.request
        error_detail = ""
        if response.status_code >= 400:
            await response.aread() # seems we need it according to the docs
            error_detail = f" - Details :{response.text}"
        logger.info(f"Response event: {request.method} {request.url} - Status {response.status_code} {error_detail}")

#### Custom Auth for httpx
class BearerAuth(Auth):
    def __init__(self, api_key:str):
        self.token = f"Bearer {api_key}" # "build" the bearer token, might be something better than that

    def auth_flow(self, request):
        # Send the request, with the bearer token in `Authentication` header.
        request.headers['Authorization'] = self.token
        yield request