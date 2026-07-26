from datetime import datetime, timedelta, timezone
from jose import  jwt
from passlib.context import CryptContext
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#хешируем пароль, для того чтобы не хранить его в откытом доступе
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
# проверяем, совпадает ли введеный пароль сохраненому хэшу
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
#как только пользователь входит в систему, создаем JWT-токен
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
# расшифровываем JWT-токен
def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])