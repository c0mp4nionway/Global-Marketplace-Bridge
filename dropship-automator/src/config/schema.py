from pydantic import BaseModel, Field
from typing import Optional

class APIConfig(BaseModel):
    app_key: str = Field(..., description="API key for the application")
    app_secret: str = Field(..., description="API secret for the application")

class EnvironmentConfig(BaseModel):
    production: APIConfig
    sandbox: APIConfig

class Config(BaseModel):
    ebay: EnvironmentConfig
    aliexpress: EnvironmentConfig
    markup_percent: float = Field(30.0, description="Default markup percentage for products")
    sync_interval_hours: int = Field(6, description="Interval for syncing stocks in hours")
    use_sandbox: bool = Field(True, description="Use sandbox environment for testing")