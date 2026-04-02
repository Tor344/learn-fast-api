#Остановился на https://fastapi.tiangolo.com/ru/tutorial/security/get-current-user/  Создать модель пользователял
#
from typing import Annotated

import uvicorn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import pydantic
from pydantic import BaseModel

#print(Hello word)
engine = create_async_engine("sqlite+aiosqlite:///datebase.db")

new_session = async_sessionmaker(engine, expire_on_commit=False)



async def get_session():
    async with new_session() as session:
        yield session



class Base(DeclarativeBase):
    pass



class BookModel(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] 
    author: Mapped[str]





from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer


SessionDep = Annotated[AsyncSession, Depends(get_session)]
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def main():
    return {}


@app.get("/items/")
async def admin(token: Annotated[str,  Depends(oauth2_scheme)]):
    return {"tocken": token }






class BookAddSchema(BaseModel):
    title:str
    author: str


class BookSchema(BookAddSchema):
    id: int


# @app.post("/add_book")
# async def add_book(date: BookAddSchema, session:SessionDep):
#     new_book = BaseModel(
#         title= date.title,
#         author = date.author
#     )
#     session.add(new_book)
#     await session.commit()    
#     return {"ok": True}








if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",port=8000, reload=True)