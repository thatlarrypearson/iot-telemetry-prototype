# server.py
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    id: int = None
    name: str
    description: str = None
    price: float
    tax: float = None


app = FastAPI()

fake_items_db = [{id: 1, "item_name": "Foo"}, {id: 2, "item_name": "Bar"}, {id: 3, "item_name": "Baz"}]

@app.get("/items/")
async def item_get_all(skip: int = 0, limit: int = 100):
    # DB Query
    return fake_items_db[skip : skip + limit]

@app.get("/items/{id}")
async def item_get(id: int, item: Item):
    # need to queery item using item.id as PKEY value
    return {**item.dict()}

@app.post("/items/")
async def item_post(item: Item):
    # on insert, item.id is provided by DB
    return {**item.dict()}


@app.put("/items/{id}")
async def item_put(id: int, item: Item):
    return {**item.dict()}

@app.delete("/items/{id}")
async def item_delete(id: int):
    return {"id": id}