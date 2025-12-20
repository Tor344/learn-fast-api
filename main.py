from fastapi import FastAPI
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str
    price: int = Field(...,ge=0)


app = FastAPI()

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
    return {"item_id": item_id, "q": q}