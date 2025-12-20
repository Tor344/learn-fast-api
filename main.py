from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return {}

@app.get("/hello")
def hello():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def items(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}