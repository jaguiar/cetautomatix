# definitely inspired by AlbertApi
from app.clients import AlbertClient
from app.config.settings import Settings, HttpxSettings
from app.config.logging import logger
from httpx import AsyncClient, Limits, Timeout
from app.clients._genericasynhttpclient import GenericAsyncHttpClient

# from app.config.variables import


class ClientsManager:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def set(self):
        # self.models = ModelClients(settings=self.settings)

        # we use a "global httpx client", it seems to be the recommended way : https://github.com/encode/httpx/issues/1042
        # the ClientManager is responsible for instantiating it which coud definitely be discussed
        logger.debug("Creating httpx client...")
        self.httpx_client = self.initGlobalHttpxClient(httpx_settings=self.settings.httpx)
        logger.debug("Creating AlbertAPI client...")
        self.albert = AlbertClient(settings=self.settings.albert_api, httpx_client=self.httpx_client)

    @staticmethod
    def initGlobalHttpxClient(httpx_settings: HttpxSettings) -> AsyncClient:
        limits = Limits(
            max_keepalive_connections=httpx_settings.max_keepalive_connections,
            max_connections=httpx_settings.max_connections,
        )
        timeouts = Timeout(timeout=httpx_settings.timeout)
        default_headers = None
        event_hooks = {
            "request": [GenericAsyncHttpClient.log_request],
            "response": [GenericAsyncHttpClient.log_response, GenericAsyncHttpClient.raise_on_4xx_5xx],
        }
        return AsyncClient(headers=default_headers, limits=limits, event_hooks=event_hooks)

    # FIXME there should be a better way to do this with introspection or something else
    def get_clients_list(self):
        return ["albert", "httpx_client"]

    async def clear(self):
        await self.httpx_client.aclose()
