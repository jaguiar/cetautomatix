from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional
from pydantic import Field, SecretStr, BaseModel

from functools import lru_cache

class AlbertApiSettings(BaseModel):  
    base_url: str
    api_key: SecretStr #= Field(exclude=True) #hopefully secure, exclude=True is probably useless here?!
    max_cerfas_per_request: int = 20
    language_model: Literal["AgentPublic/llama3-instruct-guillaumetell", "PleIAs/Cassandre-RAG"] = "AgentPublic/llama3-instruct-guillaumetell"

# httpx client
class HttpxSettings(BaseModel):  
    max_keepalive_connections: int = 5
    max_connections: int = 10
    timeout: float = 30.0

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter='__')

    # app info
    app_name: str = "Cétautomatix API"
    creator_email: Optional[str] = None

    # logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "WARNING"

    # albert api
    albert_api: AlbertApiSettings

    # httpx client
    httpx: HttpxSettings

    

### FIXME validate stuff better than that (url...)

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
