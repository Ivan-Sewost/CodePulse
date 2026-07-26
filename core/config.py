#читаем все, что находится в .env, превращаем их в объекты, проверяем, что все переменные заданы
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    #указания для поиска в файле .енв
    class Config:
        env_file = ".env"

settings = Settings()
"""необходимо для безопасности, ключи и пароле не хранятся в коде.
Можно запустить в другой БД, с помощью .енв.
Если будет ошибка, то Pydantyc её выбросит на старте"""