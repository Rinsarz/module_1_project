from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = 'sqlite:///D:\chat_app.db'
