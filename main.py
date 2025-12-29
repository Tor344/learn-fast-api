import asyncio
from typing import Annotated

from fastapi import FastAPI, HTTPException,Depends,File,UploadFile
from pydantic import BaseModel, Field
from sqlmodel import Field as _Field
from sqlmodel import  Session, SQLModel, create_engine


NAME_DB = "database.db"
SQL_URL = f"sqlite:///{NAME_DB}"

connect_args = {"check_same_thread": False}
engine = create_engine(SQL_URL, connect_args=connect_args)

class Hero(SQLModel, table=True):
    id: int | None = _Field(default=None, primary_key=True)
    name: str = _Field(index=True)
    age: int | None = _Field(default=None, index=True)
    secret_name: str

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


class Product(BaseModel):
    name: str
    price: int = Field(...,ge=0)


app = FastAPI()


@app.on_event("startup")
async def startup():
    create_db_and_tables()

@app.get("/")
def main():
    return {}


@app.get("/hello")
def hello():
    return {"message": "Hello World"}


@app.post("/items/")
def items(product: Product):
    return {"name": product.name, "price": product.price}


@app.get("/items/{item_id}")
def items(item_id: int, q: str | None = None):
    if q == "105 OR 1=1":
        raise HTTPException(status_code=401, detail="You are bad men")
    return {"item_id": item_id, "q": q}

@app.get("/users/")
def user(session: SessionDep):
    return {"massage": "connected"}

@app.get("/slow/")
async def slow():
    await asyncio.sleep(1)
    return {"message": "slow working"}


@app.post("/upload/")
def upload(file: Annotated[bytes, File()]):
    return {"file": len(file)}


@app.get("/CD_work")
def cd_work():
    return {"message": "True"}