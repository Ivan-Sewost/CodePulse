from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from core.security import hash_password, verify_password,create_access_token

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register(self, email: str, username: str, password: str) -> User:
        #проверяем существует ли пользователь
        result = await self.session.execute(
            select(User).where((User.email == email) | (User.username == username))
        )
        existing_user = result.scalar_one_or_none()


        if existing_user:
            raise ValueError("Пользователь с таким адресом электронной почты или именем уже существует")

        #создаем пользователя
        hashed_password = hash_password(password)
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
        )
        #Сохраняем в БД
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


    async def login(self, email: str, password: str) -> str:
        #ищем пользователя по email
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        #проверяем, что пользоваетель существует
        if not user:
            raise ValueError("Неверный адрес электронной почты или пароль")
        # проверяем пароль
        if not verify_password(password, user.hashed_password):
            raise ValueError ("Неверный адрес электронной почты или пароль")
        #создаем токен
        token = create_access_token({"sub": str(user.id)})
        return token