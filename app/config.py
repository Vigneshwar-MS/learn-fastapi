from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_name: str
    database_host: str
    database_port: str
    secret_key: str
    algorithm: str
    access_token_expiry_time: str

    class Config:
        env_file = ".env"


settings = Settings()