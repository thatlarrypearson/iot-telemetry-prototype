#
from collections import ChainMap
from typing import Dict
from inspect import getmro, isclass

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    id: int = None
    name: str
    description: str = None
    price: float
    tax: float = None


def get_data_model(type_: 'ModelOrDc') -> Dict[str, classmethod]:
    all_attributes = ChainMap(*[cls.__dict__ for cls in type_.__mro__])
    return {k: v for k, v in all_attributes.items()}

for k in get_data_model(Item):
    print(k)

# Class.__annotations__ is a list of dictionaries containing keys representing
# the field name and a Class identifying the field type
#   {"key": Class}
print(Item.__annotations__)

print(getmro(Item))

print(Item.__name__)

print(getmro(BaseModel))

print(BaseModel.__name__)

def is_pydantic_model_class(cls):
    if not isclass(cls):
        print('not a class')
        return False
    if BaseModel not in getmro(cls):
        print('not BaseModel child')
        return False
    return True

if not is_pydantic_model_class('string'):
    print('not pydantic model or not class')

if not is_pydantic_model_class(ChainMap):
    print('not pydantic model or not class')

if is_pydantic_model_class(Item):
    print('Item is a pydantic model class')

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